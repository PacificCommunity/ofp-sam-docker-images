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
import time

# Exact additional targets are defined by pinned d812 CMake sources retained in
# metadata-v3: batched-bench, llama-bench, common, and server. No generic suffix.
LIBRARY=re.compile(r'lib(?:llama(?:-batched-bench-impl|-bench-impl|-common|-server-impl)?|mtmd|ggml(?:-base|-cpu(?:-[A-Za-z0-9_-]+)?)?)\.so(?:\.[0-9]+)*\Z')
EXECUTABLES={'llama','llama-server'}


def identity(info):
    # Reading may change atime; all identity/content/ownership fields stay fixed.
    return tuple(getattr(info,key) for key in ('st_dev','st_ino','st_mode','st_nlink','st_uid','st_gid','st_size','st_mtime_ns','st_ctime_ns'))


R_QUERY=r'''stopifnot(getRversion() >= "4.5.0", requireNamespace("RTMB", quietly=TRUE), requireNamespace("jsonlite", quietly=TRUE), packageVersion("jsonlite") >= "2.0.0"); cat(jsonlite::toJSON(list(version=as.character(getRversion()), home=R.home(), lib_paths=.libPaths(), RTMB=list(version=as.character(packageVersion("RTMB")),path=find.package("RTMB")), jsonlite=list(version=as.character(packageVersion("jsonlite")),path=find.package("jsonlite"))),auto_unbox=TRUE))'''


def command(argv,env=None):
    result=subprocess.run(argv,check=True,timeout=15,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    if len(result.stdout)+len(result.stderr)>65536:raise ValueError('Small version smoke output exceeds64KiB')
    return dict(argv=argv,stdout=result.stdout.decode('utf-8'),stderr=result.stderr.decode('utf-8'),timeout_seconds=15)


def ordinary(path,dir_fd=None,name=None,deadline=None,clock=time.monotonic):
    path=Path(path);name=str(path) if name is None else name
    info=os.stat(name,dir_fd=dir_fd,follow_symlinks=False)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1:raise ValueError('Ordinary single-link image file required: '+str(path))
    if info.st_size>536870912:raise ValueError('Image smoke file exceeds512MiB')
    digest=hashlib.sha256();count=0
    fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=dir_fd)
    with os.fdopen(fd,'rb') as stream:
        before=os.fstat(stream.fileno())
        if identity(before)!=identity(info):raise ValueError('Image file changed before bounded hashing')
        while True:
            if deadline is not None and clock()>=deadline:raise ValueError('Cooperative closure inventory deadline exhausted')
            block=stream.read(1048576)
            if not block:break
            digest.update(block);count+=len(block)
        after=os.fstat(stream.fileno())
    if count!=info.st_size or identity(before)!=identity(after) or identity(os.stat(name,dir_fd=dir_fd,follow_symlinks=False))!=identity(before):raise ValueError('Changed image file during smoke')
    return dict(path=str(path),bytes=count,sha256=digest.hexdigest(),mode=format(stat.S_IMODE(info.st_mode),'04o'))


def layout_metadata(fd,names):
    rows=[]
    for name in names[:1024]:
        mode=os.stat(name,dir_fd=fd,follow_symlinks=False).st_mode
        kind=('ordinary' if stat.S_ISREG(mode) else 'symlink' if stat.S_ISLNK(mode) else 'directory' if stat.S_ISDIR(mode) else 'fifo' if stat.S_ISFIFO(mode) else 'socket' if stat.S_ISSOCK(mode) else 'other_special')
        rows.append(dict(name=name[:160],name_truncated=len(name)>160,kind=kind))
    report=dict(status='UNQUALIFIED_CPU_LAYOUT_METADATA_ONLY',scope='Flat name/kind observation only; no accepted type/alias/hash/CPU/ABI closure',observed_entries=len(names),complete_names=len(rows)==len(names) and all(not row['name_truncated'] for row in rows),files=rows)
    while len(json.dumps(report,ensure_ascii=True,sort_keys=True).encode())>65536:
        rows.pop();report['complete_names']=False
    return report


def engine_inventory(root,clock=time.monotonic,diagnostic=None):
    """Pinned CPU server scope: flat llama/llama-server and CPU shared libraries.

    The source cp-P retains library aliases. Their literal basename targets must
    resolve within this closed flat inventory to ordinary single-link files.
    Actual filenames/layout remain unobserved until this complete build gate.
    """
    root=Path(root);deadline=clock()+15
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        names=sorted(os.listdir(fd))
        if diagnostic is not None:diagnostic(layout_metadata(fd,names))
        if not 1<=len(names)<=1024 or not EXECUTABLES.issubset(names):raise ValueError('Exact flat CPU executable scope required')
        for name in names:
            if len(name)>160 or (name not in EXECUTABLES and not LIBRARY.fullmatch(name)):raise ValueError('Unexpected CPU server closure member: '+name)
        ordinary_rows={};aliases={};initial={name:os.stat(name,dir_fd=fd,follow_symlinks=False) for name in names}
        total=0
        for name in names:
            if clock()>=deadline:raise ValueError('Cooperative closure inventory deadline exhausted')
            info=initial[name]
            if stat.S_ISREG(info.st_mode):
                if name in EXECUTABLES and not info.st_mode&0o111:raise ValueError('Ordinary CPU executable mode required')
                row=ordinary(root/name,dir_fd=fd,name=name,deadline=deadline,clock=clock);row['kind']='ordinary';ordinary_rows[name]=row;total+=row['bytes']
                if total>536870912:raise ValueError('Unique CPU closure files exceed512MiB')
            elif stat.S_ISLNK(info.st_mode) and LIBRARY.fullmatch(name):
                target=os.readlink(name,dir_fd=fd)
                if not LIBRARY.fullmatch(target) or target not in initial:raise ValueError('Library alias must target an existing flat CPU library basename')
                aliases[name]=target
            else:raise ValueError('CPU closure refuses executable aliases/directories/special files')
        rows=[]
        for name in names:
            if name not in aliases:rows.append(ordinary_rows[name]);continue
            current=name;seen=set();chain=[]
            while current in aliases:
                if current in seen or len(seen)>=64:raise ValueError('Library alias cycle or excessive chain')
                seen.add(current);chain.append(current);current=aliases[current]
            if current not in ordinary_rows or not LIBRARY.fullmatch(current):raise ValueError('Library alias has no ordinary confined target')
            rows.append(dict(path=str(root/name),kind='library_alias',raw_target=aliases[name],ordinary_target=ordinary_rows[current],alias_chain=chain))
        if sorted(os.listdir(fd))!=names or any(identity(os.stat(name,dir_fd=fd,follow_symlinks=False))!=identity(initial[name]) for name in names) or any(os.readlink(name,dir_fd=fd)!=target for name,target in aliases.items()):raise ValueError('CPU closure changed during inventory')
        if clock()>=deadline:raise ValueError('Cooperative closure inventory deadline exhausted')
        return dict(scope='Pinned official CPU server flat /app copies: ordinary llama/llama-server, libllama/core/common/server-impl/bench-impl/batched-bench-impl, libmtmd/libggml/base/cpu shared libraries and confined library aliases; no claimed full ELF dependency qualification',files=rows,unique_ordinary_bytes=total,ordinary_files=len(ordinary_rows),aliases=len(aliases),cooperative_seconds=15)
    finally:os.close(fd)


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
        engine=engine_inventory('/opt/llama',diagnostic=lambda row:print(json.dumps(row,ensure_ascii=True,sort_keys=True),flush=True))
        node=command(['/usr/local/bin/node','--version'])
        if node['stdout'].strip()!='v24.21.0':raise ValueError('Node version differs from publisher pin')
        env=dict(os.environ,LD_LIBRARY_PATH='/opt/llama')
        llama=command(['/opt/llama/llama-server','--version'],env=env);version=llama['stdout']+llama['stderr']
        if not re.search(r'\b11429\b',version) or 'd812350' not in version:raise ValueError('CPU server version/revision differs from observed immutable OCI/source')
        model=ordinary('/opt/kimsa/models/qwen3-0.6b.gguf');receipt=json.loads(Path('/opt/kimsa/provenance/MODEL-INPUT.json').read_text())
        if model['bytes']!=522640096 or model['sha256']!='7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa' or model['mode']!='0444' or receipt['status']!='PASS_EXACT_PUBLIC_INPUT_ONLY' or receipt['sha256']!=model['sha256']:raise ValueError('Readonly exact full model input required')
        report.update(status='PASS_BUILD_EXECUTABLE_ABI_SMOKE_ONLY',Node=node,llama_server=llama,engine_files=engine,Node_file=ordinary('/usr/local/bin/node'),model_file=model,base_R_unchanged=True,model_loading=False,inference=False,server_api=False)
    raw=(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>65536:raise ValueError('Small smoke report exceeds64KiB')
    with args.output.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    print(json.dumps(dict(status=report['status'],report=str(args.output),sha256=hashlib.sha256(raw).hexdigest()),sort_keys=True),flush=True)


if __name__=='__main__':main()
