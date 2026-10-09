"""Bounded public OCI JSON/source metadata only; no layer/runtime downloads."""
import hashlib
import json
from pathlib import Path
import ssl
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parent
LIMIT=1048576
ACCEPT=', '.join(['application/vnd.oci.image.index.v1+json','application/vnd.docker.distribution.manifest.list.v2+json','application/vnd.oci.image.manifest.v1+json','application/vnd.docker.distribution.manifest.v2+json'])
TOKENS={}
RECEIPTS=[]


def bounded(url,headers=None):
    request=urllib.request.Request(url,headers=dict(headers or {},**{'User-Agent':'kimsa-public-image-metadata/1','Accept-Encoding':'identity'}))
    with urllib.request.urlopen(request,timeout=20,context=ssl.create_default_context()) as response:
        raw=response.read(LIMIT+1)
        if len(raw)>LIMIT:raise ValueError('Public metadata body exceeds one MiB')
        return raw,{key:response.headers.get(key) for key in ('Content-Type','Content-Length','Docker-Content-Digest')},response.status


def registry(url,host,repo):
    headers={'Accept':ACCEPT}
    if (host,repo) in TOKENS:headers['Authorization']='Bearer '+TOKENS[host,repo]
    try:return bounded(url,headers)
    except urllib.error.HTTPError as error:
        if error.code!=401:raise
        # No user credentials/config read. Public pull token remains in memory;
        # neither token response nor Authorization headers/redirect URL logged.
        token_url=('https://ghcr.io/token?service=ghcr.io&scope=repository:'+repo+':pull' if host=='ghcr.io' else
                   'https://auth.docker.io/token?service=registry.docker.io&scope=repository:'+repo+':pull')
        raw,_,_=bounded(token_url)
        token=json.loads(raw).get('token') or json.loads(raw).get('access_token')
        if not isinstance(token,str) or not token:raise ValueError('Anonymous public registry token unavailable')
        TOKENS[host,repo]=token;headers['Authorization']='Bearer '+token
        return bounded(url,headers)


def save(name,url,raw,headers,status,expected=None):
    digest='sha256:'+hashlib.sha256(raw).hexdigest()
    if expected is not None and expected!=digest:raise ValueError('Exact OCI descriptor/body digest mismatch')
    reported=headers.get('Docker-Content-Digest')
    if reported and reported!=digest:raise ValueError('OCI response digest/header mismatch')
    path=ROOT/name
    with path.open('xb') as stream:stream.write(raw)
    row=dict(file=name,url=url,bytes=len(raw),sha256=digest.split(':')[1],http_status=status,selected_headers=headers,scope='Public source/OCI JSON only; normal trusted TLS; anonymous pull-token held only in memory; no layers/binaries/models or user credentials')
    RECEIPTS.append(row)
    return json.loads(raw),digest


def image(name,host,repo,tag):
    registry_host='registry-1.docker.io' if host=='docker.io' else host
    root='https://'+registry_host+'/v2/'+repo
    url=root+'/manifests/'+tag
    raw,headers,status=registry(url,host,repo)
    value,digest=save(name+'-index.json',url,raw,headers,status)
    if 'manifests' in value:
        matches=[row for row in value['manifests'] if row.get('platform',{}).get('os')=='linux' and row.get('platform',{}).get('architecture')=='amd64']
        if len(matches)!=1:raise ValueError('Exactly one Linux amd64 child required')
        selected=matches[0]
        url=root+'/manifests/'+selected['digest']
        raw,headers,status=registry(url,host,repo)
        manifest,child=save(name+'-amd64-manifest.json',url,raw,headers,status,selected['digest'])
    else:
        manifest,child=value,digest
    config=manifest['config']
    if config['mediaType'] not in ('application/vnd.oci.image.config.v1+json','application/vnd.docker.container.image.v1+json'):
        raise ValueError('Only declared JSON config blob may be requested; no layer body')
    url=root+'/blobs/'+config['digest']
    raw,headers,status=registry(url,host,repo)
    cfg,configdigest=save(name+'-amd64-config.json',url,raw,headers,status,config['digest'])
    if cfg['os']!='linux' or cfg['architecture']!='amd64':raise ValueError('Config platform mismatch')
    return dict(observed_tag=host+'/'+repo+':'+tag,index_digest=digest,amd64_manifest_digest=child,config_digest=configdigest,labels=cfg.get('config',{}).get('Labels'),entrypoint=cfg.get('config',{}).get('Entrypoint'),command=cfg.get('config',{}).get('Cmd'),working_dir=cfg.get('config',{}).get('WorkingDir'),layers=manifest['layers'])


def main():
    for name,host,repo,tag in [('llama-server','ghcr.io','ggml-org/llama.cpp','server-b11429'),('node','docker.io','library/node','24.21.0-bookworm-slim'),('base','ghcr.io','pacificcommunity/tuna-flow','sha256:c87f1f6d9d4f62dc447844b58afe35f96af175bf933cb6cffbbbe39a59172360')]:
        try:
            record=image(name,host,repo,tag)
            with (ROOT/(name+'-selection.json')).open('x') as stream:json.dump(record,stream,indent=2,sort_keys=True);stream.write('\n')
            print(json.dumps(dict(name=name,**{k:v for k,v in record.items() if k!='layers'}),sort_keys=True),flush=True)
        except Exception as error:
            failure=dict(name=name,type=type(error).__name__,failure=str(error))
            with (ROOT/(name+'-refusal.json')).open('x') as stream:json.dump(failure,stream,indent=2);stream.write('\n')
            print(json.dumps(failure),flush=True)
    for filename,url in [('llama-docker.md','https://raw.githubusercontent.com/ggml-org/llama.cpp/d81235049384534c167caea52b85a694f6103d14/docs/docker.md'),('llama-cpu.Dockerfile','https://raw.githubusercontent.com/ggml-org/llama.cpp/d81235049384534c167caea52b85a694f6103d14/.devops/cpu.Dockerfile'),('llama-docker.yml','https://raw.githubusercontent.com/ggml-org/llama.cpp/d81235049384534c167caea52b85a694f6103d14/.github/workflows/docker.yml')]:
        raw,headers,status=bounded(url)
        path=ROOT/filename
        with path.open('xb') as stream:stream.write(raw)
        RECEIPTS.append(dict(file=filename,url=url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),http_status=status,scope='Pinned public primary source text; not executed'))
    with (ROOT/'metadata-manifest.json').open('x') as stream:json.dump(RECEIPTS,stream,indent=2,sort_keys=True);stream.write('\n')


if __name__=='__main__':main()
