"""Inert flat CPU library alias/refusal fixtures; no executable invocation."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import stat
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

ROOT=None
spec=importlib.util.spec_from_file_location('image_smoke',Path(__file__).with_name('smoke.py'))
smoke=importlib.util.module_from_spec(spec);spec.loader.exec_module(smoke)


class Closure(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT);self.root=Path(self.temp.name)
        for name in ('llama','llama-server'):(self.root/name).write_bytes(b'inert executable fixture');(self.root/name).chmod(0o500)
        (self.root/'libllama.so.0').write_bytes(b'inert ordinary library')
    def tearDown(self):self.temp.cleanup()
    def inventory(self,**kwargs):return smoke.engine_inventory(self.root,**kwargs)
    def refused(self):
        with self.assertRaises((ValueError,OSError)):self.inventory()
    def test_complete_ordinary_flat_inventory(self):
        report=self.inventory();self.assertEqual(report['ordinary_files'],3);self.assertEqual(report['aliases'],0)
        self.assertEqual({Path(row['path']).name for row in report['files']},{'llama','llama-server','libllama.so.0'})
        self.assertEqual(report['unique_ordinary_bytes'],sum(path.stat().st_size for path in self.root.iterdir()))
    def test_single_library_alias_retains_raw_target_and_target_hash(self):
        (self.root/'libllama.so').symlink_to('libllama.so.0');report=self.inventory();row=next(row for row in report['files'] if row['kind']=='library_alias')
        self.assertEqual(row['raw_target'],'libllama.so.0');self.assertEqual(row['ordinary_target']['sha256'],hashlib.sha256(b'inert ordinary library').hexdigest())
        self.assertEqual(report['ordinary_files'],3);self.assertEqual(report['aliases'],1);self.assertEqual(row['alias_chain'],['libllama.so'])
    def test_confined_multihop_alias_order(self):
        (self.root/'libllama.so.0').rename(self.root/'libllama.so.0.1');(self.root/'libllama.so.0').symlink_to('libllama.so.0.1');(self.root/'libllama.so').symlink_to('libllama.so.0')
        row=next(row for row in self.inventory()['files'] if Path(row['path']).name=='libllama.so')
        self.assertEqual(row['alias_chain'],['libllama.so','libllama.so.0']);self.assertEqual(Path(row['ordinary_target']['path']).name,'libllama.so.0.1')
    def test_absolute_library_alias_refused(self):
        (self.root/'libllama.so').symlink_to(self.root/'libllama.so.0');self.refused()
    def test_parent_escape_alias_refused(self):
        (self.root/'libllama.so').symlink_to('../libllama.so.0');self.refused()
    def test_slash_alias_refused(self):
        (self.root/'libllama.so').symlink_to('./libllama.so.0');self.refused()
    def test_dangling_alias_refused(self):
        (self.root/'libllama.so').symlink_to('libllama.so.99');self.refused()
    def test_cycle_refused(self):
        (self.root/'libllama.so').symlink_to('libllama.so.1');(self.root/'libllama.so.1').symlink_to('libllama.so');self.refused()
    def test_directory_alias_refused(self):
        (self.root/'libllama.so.1').mkdir();(self.root/'libllama.so').symlink_to('libllama.so.1');self.refused()
    def test_fifo_refused_without_open_or_block(self):
        os.mkfifo(self.root/'libggml.so');self.refused()
    def test_socket_refused(self):
        with socket.socket(socket.AF_UNIX) as sock:sock.bind(str(self.root/'libggml.so'));self.refused()
    def test_executable_alias_refused(self):
        (self.root/'llama-server').unlink();(self.root/'llama-server').symlink_to('llama');self.refused()
    def test_other_entry_and_gpu_backend_refused(self):
        for name in ('README.txt','libggml-cuda.so','libggml-vulkan.so'):
            (self.root/name).write_bytes(b'inert unexpected');self.refused();(self.root/name).unlink()
    def test_library_hardlink_refused(self):
        os.link(self.root/'libllama.so.0',self.root/'libllama.so.1');self.refused()
    def test_root_symlink_refused(self):
        link=self.root/'alias';link.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(OSError):smoke.engine_inventory(link)
    def test_missing_required_executable_refused(self):
        (self.root/'llama').unlink();self.refused()
    def test_expired_cooperative_inventory_refused(self):
        class Clock:
            def __init__(self):self.calls=0
            def __call__(self):self.calls+=1;return 0 if self.calls==1 else 15
        with self.assertRaises(ValueError):self.inventory(clock=Clock())
    def test_changed_regular_target_refused(self):
        original=smoke.ordinary
        def change(path,**kwargs):
            report=original(path,**kwargs)
            if Path(path).name=='libllama.so.0':Path(path).write_bytes(b'changed after hashing')
            return report
        with patch.object(smoke,'ordinary',change):self.refused()
    def test_pinned_CMake_extra_libraries_ordinary(self):
        names=('libllama-batched-bench-impl.so','libllama-bench-impl.so','libllama-common.so','libllama-server-impl.so')
        for name in names:(self.root/name).write_bytes(b'inert pinned CMake library')
        rows=self.inventory()['files']
        for name in names:
            row=next(row for row in rows if Path(row['path']).name==name)
            self.assertEqual(row['kind'],'ordinary');self.assertEqual(row['sha256'],hashlib.sha256(b'inert pinned CMake library').hexdigest())
    def test_pinned_CMake_extra_library_aliases(self):
        names=('libllama-batched-bench-impl.so','libllama-bench-impl.so','libllama-common.so','libllama-server-impl.so')
        for name in names:
            (self.root/(name+'.1')).write_bytes(b'inert target');(self.root/name).symlink_to(name+'.1')
        rows=self.inventory()['files']
        for name in names:
            row=next(row for row in rows if Path(row['path']).name==name)
            self.assertEqual(row['raw_target'],name+'.1');self.assertEqual(row['ordinary_target']['sha256'],hashlib.sha256(b'inert target').hexdigest())
    def test_layout_diagnostic_precedes_refusal_without_qualification(self):
        (self.root/'unaccepted-member').write_bytes(b'inert');observed=[]
        with self.assertRaises(ValueError):smoke.engine_inventory(self.root,diagnostic=observed.append)
        self.assertEqual(len(observed),1);report=observed[0]
        self.assertEqual(report['status'],'UNQUALIFIED_CPU_LAYOUT_METADATA_ONLY');self.assertTrue(report['complete_names'])
        self.assertEqual(next(row for row in report['files'] if row['name']=='unaccepted-member')['kind'],'ordinary')
        self.assertTrue(all(set(row)=={'name','name_truncated','kind'} for row in report['files']))
    def test_exact_encoded_diagnostic_line_boundary_and_truncation(self):
        line=lambda row:(json.dumps(row,ensure_ascii=True,sort_keys=True)+'\n').encode()
        # Metadata-only fake stat, no filesystem body, qualification or binary.
        with patch.object(smoke.os,'stat',return_value=SimpleNamespace(st_mode=stat.S_IFREG)):
            names=['x']*400;baseline=smoke.layout_metadata(-1,names)
            gap=65536-len(line(baseline));self.assertGreaterEqual(gap,0);self.assertLessEqual(gap,400*159)
            for index in range(400):
                padding=min(gap,159);names[index]='x'*(1+padding);gap-=padding
            self.assertEqual(gap,0)
            exact=smoke.layout_metadata(-1,names);self.assertEqual(len(line(exact)),65536);self.assertTrue(exact['complete_names'])
            names[next(index for index,name in enumerate(names) if len(name)<160)]+='y'
            truncated=smoke.layout_metadata(-1,names)
            self.assertLessEqual(len(line(truncated)),65536);self.assertFalse(truncated['complete_names']);self.assertEqual(truncated['observed_entries'],400);self.assertLess(len(truncated['files']),400)


def main():
    global ROOT
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',required=True,type=Path);args=parser.parse_args();ROOT=args.output_dir
    if sys.platform!='linux' or not sys.dont_write_bytecode:raise SystemExit('Inert Linux Python-B fixtures only')
    if not ROOT.is_absolute() or ROOT.is_symlink() or not ROOT.is_dir():raise ValueError('Fresh absolute ordinary fixture root required')
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Closure);count=suite.countTestCases();result=unittest.TextTestRunner(verbosity=2).run(suite)
    report=dict(status='PASS_INERT_CPU_CLOSURE_FIXTURES_ONLY' if result.wasSuccessful() and not result.skipped else 'FAILED',tests=count,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),binary_execution=False,network=False)
    with (ROOT/'FIXTURES.json').open('xb') as stream:stream.write((json.dumps(report,sort_keys=True)+'\n').encode());stream.flush();os.fsync(stream.fileno())
    print(json.dumps(report,sort_keys=True),flush=True);return 0 if result.wasSuccessful() and not result.skipped else 1


if __name__=='__main__':raise SystemExit(main())
