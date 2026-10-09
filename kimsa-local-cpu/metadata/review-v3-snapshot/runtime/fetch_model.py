"""One build-only acquisition of a pinned public GGUF; never downloads at startup."""
import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path
import ssl
import stat
import struct
import sys
import time
import urllib.parse
import urllib.request

PIN=dict(url='https://registry.ollama.ai/v2/library/qwen3/blobs/sha256:7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa',bytes=522640096,sha256='7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa',filename='qwen3-0.6b.gguf')
SECONDS=110


class Refusal(ValueError):pass


class HTTPSRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):self.hosts=[]
    def redirect_request(self,request,fp,code,message,headers,newurl):
        parsed=urllib.parse.urlsplit(newurl)
        if parsed.scheme!='https' or parsed.username is not None or parsed.password is not None or len(self.hosts)>=3:
            raise Refusal('Only at most three verified HTTPS publisher redirects; no downgrade/retry')
        self.hosts.append(parsed.hostname)
        return super().redirect_request(request,fp,code,message,headers,newurl)


def tick(deadline,clock):
    if not math.isfinite(deadline) or clock()>=deadline:raise Refusal('Cooperative110 build-input acceptance exhausted')


def directory(path):
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts:raise Refusal('Absolute ordinary owned build directory required')
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for name in path.parts[1:]:
            child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=child
        info=os.fstat(fd)
        if info.st_uid!=os.getuid() or stat.S_IMODE(info.st_mode)!=0o700:raise Refusal('Fresh owned0700 build-input directory required')
        return fd
    except BaseException:os.close(fd);raise


def metadata(fd,name,value):
    raw=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>65536:raise Refusal('Small build-input receipt exceeds64KiB')
    target=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=fd)
    with os.fdopen(target,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    os.fsync(fd)
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def fetch(destination,pin=None,opener=None,clock=None):
    """Testable inert dependency seam; production CLI permits only literal PIN."""
    pin=PIN if pin is None else pin;clock=time.monotonic if clock is None else clock
    start=clock();deadline=start+SECONDS;fd=directory(destination)
    count,digest,prefix,published,partial=0,hashlib.sha256(),b'',False,False
    redirects=HTTPSRedirects()
    report=dict(status='REFUSED',publisher_url=pin['url'],expected_bytes=pin['bytes'],expected_sha256=pin['sha256'],bytes_received=0,attempts=1,retries=0,scope='Public immutable build input only; no model loading/inference, parent-job qualification or output-cap exception')
    try:
        if set(pin)!=set(PIN) or type(pin['bytes']) is not int or not 24<=pin['bytes']<=536870912 or pin['filename']!='qwen3-0.6b.gguf' or not re.fullmatch('[a-f0-9]{64}',pin['sha256']):
            raise Refusal('Exact bounded model pin/schema required')
        parsed=urllib.parse.urlsplit(pin['url'])
        if parsed.scheme!='https' or parsed.username is not None or parsed.password is not None:raise Refusal('Verified public HTTPS input only')
        for name in (pin['filename'],'.model-download','MODEL-INPUT.json','MODEL-INPUT.partial.json','MODEL-REFUSED.json'):
            try:os.stat(name,dir_fd=fd,follow_symlinks=False)
            except FileNotFoundError:pass
            else:raise Refusal('Fresh destination required; no cache, replacement or retry')
    except BaseException:
        os.close(fd);raise
    try:
        tick(deadline,clock)
        if opener is None:
            opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=ssl.create_default_context()),redirects)
        request=urllib.request.Request(pin['url'],headers={'Accept-Encoding':'identity','User-Agent':'kimsa-public-fixed-model-build/1'})
        target=os.open('.model-download',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd);partial=True
        with os.fdopen(target,'wb') as stream:
            tick(deadline,clock)
            with opener.open(request,timeout=min(10,deadline-clock())) as response:
                tick(deadline,clock)
                if response.status!=200 or response.headers.get('Content-Encoding') not in (None,'identity'):
                    raise Refusal('One successful plain publisher representation required')
                declared=response.headers.get('Content-Length')
                if declared is not None and declared!=str(pin['bytes']):raise Refusal('Publisher length differs from exact pin')
                while True:
                    tick(deadline,clock);block=response.read(65536);tick(deadline,clock)
                    if not block:break
                    count+=len(block);report['bytes_received']=count
                    if count>pin['bytes']:raise Refusal('Model exceeds exact byte pin')
                    digest.update(block);prefix=(prefix+block)[:24];stream.write(block)
                    report['received_prefix_sha256']=digest.hexdigest()
                stream.flush();os.fsync(stream.fileno());tick(deadline,clock)
                if count!=pin['bytes'] or digest.hexdigest()!=pin['sha256']:raise Refusal('Incomplete model/full byte or SHA pin mismatch')
                if len(prefix)!=24 or prefix[:4]!=b'GGUF':raise Refusal('Pinned body is not a complete GGUF header')
                version,tensors,keys=struct.unpack('<IQQ',prefix[4:])
                if version not in (2,3) or not 1<=tensors<=10000 or not 1<=keys<=10000:raise Refusal('Unsupported/implausible GGUF header; no loader qualification')
                os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno());tick(deadline,clock)
        # Exclusive hard-link publication refuses a raced destination. It shares
        # one inode briefly; no second body/copy is created or retained.
        os.link('.model-download',pin['filename'],src_dir_fd=fd,dst_dir_fd=fd,follow_symlinks=False);published=True
        os.unlink('.model-download',dir_fd=fd);partial=False
        os.fsync(fd);tick(deadline,clock)
        report.update(status='PASS_EXACT_PUBLIC_INPUT_ONLY',bytes=count,sha256=digest.hexdigest(),filename=pin['filename'],mode='0444',gguf_header=dict(version=version,tensors=tensors,metadata_keys=keys,scope='Header only; architecture/tokenizer/model compatibility unqualified'),redirect_hosts=redirects.hosts,elapsed_seconds=clock()-start,deadline_scope='Cooperative110 includes full body/hash/fsync/publication/final receipt; no hard-kernel/abrupt-loss guarantee',tls='Default verified HTTPS; no user credentials, proxy config, retries or runtime download')
        metadata(fd,'MODEL-INPUT.json',report)
        tick(deadline,clock)
        return report
    except Exception as error:
        # Never retain an executable/qualified model after a failed/late gate.
        if partial:os.unlink('.model-download',dir_fd=fd)
        if published:os.unlink(pin['filename'],dir_fd=fd)
        # metadata may fail after creating/writing/fsyncing the file. Never rely
        # on a post-return flag to revoke that incomplete acceptance receipt.
        try:os.stat('MODEL-INPUT.json',dir_fd=fd,follow_symlinks=False)
        except FileNotFoundError:pass
        else:os.rename('MODEL-INPUT.json','MODEL-INPUT.partial.json',src_dir_fd=fd,dst_dir_fd=fd)
        report.update(status='REFUSED_NO_MODEL_PUBLISHED',failure_type=type(error).__name__,failure=str(error),elapsed_seconds=clock()-start,partial_body_removed=True,received_prefix_scope='Observed prefix only, never full input authority after refusal')
        metadata(fd,'MODEL-REFUSED.json',report)
        raise Refusal(str(error)) from error
    finally:os.close(fd)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    if sys.platform!='linux' or not sys.dont_write_bytecode:raise SystemExit('Build-only Linux Python-B required; no Mac modelbody')
    try:report=fetch(args.output_dir)
    except Exception as error:
        print(json.dumps(dict(status='REFUSED_NO_MODEL_PUBLISHED',failure=str(error),retry=False)),flush=True);return 1
    print(json.dumps(report,sort_keys=True),flush=True);return 0


if __name__=='__main__':raise SystemExit(main())
