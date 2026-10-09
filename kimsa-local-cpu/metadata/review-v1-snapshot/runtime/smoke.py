"""Build-time executable/ABI smoke only: no KIMSA, models, inference or installs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import stat
import subprocess
import sys


R_QUERY=r'''stopifnot(getRversion() >= "4.5.0", requireNamespace("RTMB", quietly=TRUE), requireNamespace("jsonlite", quietly=TRUE), packageVersion("jsonlite") >= "2.0.0"); cat(jsonlite::toJSON(list(version=as.character(getRversion()), home=R.home(), lib_paths=.libPaths(), RTMB=list(version=as.character(packageVersion("RTMB")),path=find.package("RTMB")), jsonlite=list(version=as.character(packageVersion("jsonlite")),path=find.package("jsonlite"))),auto_unbox=TRUE))'''


def command(argv,env=None):
    result=subprocess.run(argv,check=True,timeout=15,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    if len(result.stdout)+len(result.stderr)>65536:raise ValueError('Small version smoke output exceeds64KiB')
    return dict(argv=argv,stdout=result.stdout.decode('utf-8'),stderr=result.stderr.decode('utf-8'),timeout_seconds=15)


def ordinary(path):
    path=Path(path);info=path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1:raise ValueError('Ordinary single-link image file required: '+str(path))
    digest=hashlib.sha256();count=0
    with path.open('rb') as stream:
        while True:
            block=stream.read(1048576)
            if not block:break
            digest.update(block);count+=len(block)
    if count!=info.st_size:raise ValueError('Changed image file during smoke')
    return dict(path=str(path),bytes=count,sha256=digest.hexdigest(),mode=format(stat.S_IMODE(info.st_mode),'04o'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',required=True,choices=('baseline','final'));parser.add_argument('--output',required=True,type=Path);parser.add_argument('--baseline',type=Path)
    args=parser.parse_args()
    if sys.platform!='linux' or platform.machine()!='x86_64' or not sys.dont_write_bytecode:raise ValueError('Linuxamd64 Python-B image build required')
    r_command=command(['Rscript','--vanilla','-e',R_QUERY]);r=json.loads(r_command['stdout'])
    report=dict(status='PASS_BASE_RUNTIME_ONLY',scope='Build smoke only; no model loading/API/KIMSA tests/scientific or speed qualification',python=dict(version=sys.version,machine=platform.machine()),R=r,R_command=r_command)
    if args.mode=='final':
        if args.baseline is None:raise ValueError('Exact base runtime report required')
        baseline=json.loads(args.baseline.read_text())
        if baseline['status']!='PASS_BASE_RUNTIME_ONLY' or r!=baseline['R']:raise ValueError('R version/dependencies/library paths changed from immutable base')
        node=command(['/usr/local/bin/node','--version'])
        if node['stdout'].strip()!='v24.21.0':raise ValueError('Node version differs from publisher pin')
        env=dict(os.environ,LD_LIBRARY_PATH='/opt/llama')
        llama=command(['/opt/llama/llama-server','--version'],env=env);version=llama['stdout']+llama['stderr']
        if not re.search(r'\b11429\b',version) or 'd812350' not in version:raise ValueError('CPU server version/revision differs from observed immutable OCI/source')
        engine=[]
        for entry in sorted(Path('/opt/llama').iterdir()):engine.append(ordinary(entry))
        model=ordinary('/opt/kimsa/models/qwen3-0.6b.gguf');receipt=json.loads(Path('/opt/kimsa/provenance/MODEL-INPUT.json').read_text())
        if model['bytes']!=522640096 or model['sha256']!='7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa' or model['mode']!='0444' or receipt['status']!='PASS_EXACT_PUBLIC_INPUT_ONLY' or receipt['sha256']!=model['sha256']:raise ValueError('Readonly exact full model input required')
        report.update(status='PASS_BUILD_EXECUTABLE_ABI_SMOKE_ONLY',Node=node,llama_server=llama,engine_files=engine,Node_file=ordinary('/usr/local/bin/node'),model_file=model,base_R_unchanged=True,model_loading=False,inference=False,server_api=False)
    raw=(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>65536:raise ValueError('Small smoke report exceeds64KiB')
    with args.output.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    print(json.dumps(dict(status=report['status'],report=str(args.output),sha256=hashlib.sha256(raw).hexdigest()),sort_keys=True),flush=True)


if __name__=='__main__':main()
