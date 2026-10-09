"""Complete inert fixtures. Run on Linux with -B; never accesses a publisher."""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=None
spec=importlib.util.spec_from_file_location('fixed_fetch',Path(__file__).with_name('fetch_model.py'))
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
BODY=b'GGUF'+struct.pack('<IQQ',3,1,1)+b'inert bytes, not a usable model'


class Clock:
    def __init__(self):self.now=0.0
    def __call__(self):return self.now


class Response(io.BytesIO):
    def __init__(self,body=BODY,headers=None,status=200):
        super().__init__(body);self.headers={} if headers is None else headers;self.status=status


class Opener:
    def __init__(self,response=None,error=None,callback=None):self.response=response or Response();self.error=error;self.calls=0;self.callback=callback
    def open(self,request,timeout):
        self.calls+=1
        if self.callback:self.callback()
        if self.error:raise self.error
        return self.response


class FixedInput(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT);self.path=Path(self.temp.name);self.path.chmod(0o700)
        self.pin=dict(helper.PIN,bytes=len(BODY),sha256=hashlib.sha256(BODY).hexdigest());self.clock=Clock()
    def tearDown(self):self.temp.cleanup()
    def fetch(self,**kwargs):return helper.fetch(self.path,pin=kwargs.pop('pin',self.pin),clock=self.clock,opener=kwargs.pop('opener',Opener()),**kwargs)
    def refuse(self,**kwargs):
        with self.assertRaises(helper.Refusal):self.fetch(**kwargs)
        self.assertFalse((self.path/self.pin['filename']).exists());self.assertFalse((self.path/'.model-download').exists())
    def test_exact_bytes_sha_readonly_single_inode_receipt(self):
        opener=Opener();report=self.fetch(opener=opener);model=self.path/self.pin['filename']
        self.assertEqual(opener.calls,1);self.assertEqual(model.read_bytes(),BODY);self.assertEqual(model.stat().st_nlink,1)
        self.assertEqual(stat.S_IMODE(model.stat().st_mode),0o444);self.assertEqual(report['status'],'PASS_EXACT_PUBLIC_INPUT_ONLY')
        self.assertEqual(json.loads((self.path/'MODEL-INPUT.json').read_text())['sha256'],self.pin['sha256'])
    def test_hash_mismatch_removes_body(self):self.refuse(pin=dict(self.pin,sha256='0'*64))
    def test_truncated_body(self):self.refuse(opener=Opener(Response(BODY[:-1])))
    def test_oversize_body(self):self.refuse(opener=Opener(Response(BODY+b'x')))
    def test_content_length_mismatch(self):self.refuse(opener=Opener(Response(headers={'Content-Length':str(len(BODY)+1)})))
    def test_content_encoding_refused(self):self.refuse(opener=Opener(Response(headers={'Content-Encoding':'gzip'})))
    def test_http_failure_no_retry(self):
        opener=Opener(Response(status=503));self.refuse(opener=opener);self.assertEqual(opener.calls,1)
    def test_network_error_no_retry(self):
        opener=Opener(error=OSError('inert failed dependency'));self.refuse(opener=opener);self.assertEqual(opener.calls,1)
    def test_bad_magic_fullhash_refused(self):
        body=b'NOPE'+BODY[4:];self.refuse(pin=dict(self.pin,sha256=hashlib.sha256(body).hexdigest()),opener=Opener(Response(body)))
    def test_unsupported_header_fullhash_refused(self):
        body=b'GGUF'+struct.pack('<IQQ',99,1,1)+BODY[24:];self.refuse(pin=dict(self.pin,sha256=hashlib.sha256(body).hexdigest()),opener=Opener(Response(body)))
    def test_zero_tensor_count_refused(self):
        body=b'GGUF'+struct.pack('<IQQ',3,0,1)+BODY[24:];self.refuse(pin=dict(self.pin,sha256=hashlib.sha256(body).hexdigest()),opener=Opener(Response(body)))
    def test_no_body_before_complete_gate(self):
        def callback():self.assertFalse((self.path/self.pin['filename']).exists())
        self.fetch(opener=Opener(callback=callback))
    def test_expired_before_request(self):
        class Expired:
            def __init__(self):self.calls=0
            def __call__(self):self.calls+=1;return 0.0 if self.calls==1 else 110.0
        self.clock=Expired();opener=Opener();self.refuse(opener=opener);self.assertEqual(opener.calls,0)
    def test_deadline_during_body_removes_partial(self):
        clock=self.clock
        class Late(Response):
            def read(self,size):clock.now=110.0;return super().read(size)
        self.refuse(opener=Opener(Late()))
    def test_final_receipt_write_crosses_deadline_revokes(self):
        original=helper.metadata
        def late(fd,name,value):
            result=original(fd,name,value)
            if name=='MODEL-INPUT.json':self.clock.now=110.0
            return result
        with patch.object(helper,'metadata',late):self.refuse()
        self.assertFalse((self.path/'MODEL-INPUT.json').exists());self.assertTrue((self.path/'MODEL-INPUT.partial.json').exists())
        self.assertEqual(json.loads((self.path/'MODEL-REFUSED.json').read_text())['status'],'REFUSED_NO_MODEL_PUBLISHED')
    def test_receipt_failure_after_creation_revokes(self):
        original=helper.metadata
        def fail(fd,name,value):
            result=original(fd,name,value)
            if name=='MODEL-INPUT.json':raise OSError('inert fsync failure after receipt creation')
            return result
        with patch.object(helper,'metadata',fail):self.refuse()
        self.assertFalse((self.path/'MODEL-INPUT.json').exists());self.assertTrue((self.path/'MODEL-INPUT.partial.json').exists())
    def test_existing_model_untouched_no_request(self):
        model=self.path/self.pin['filename'];model.write_bytes(b'prior');opener=Opener()
        with self.assertRaises(helper.Refusal):self.fetch(opener=opener)
        self.assertEqual(model.read_bytes(),b'prior');self.assertEqual(opener.calls,0);self.assertEqual(list(self.path.iterdir()),[model])
    def test_symlink_directory_refused(self):
        alias=self.path/'alias';alias.symlink_to(self.path,target_is_directory=True)
        with self.assertRaises(OSError):helper.fetch(alias,pin=self.pin,opener=Opener(),clock=self.clock)
        self.assertEqual(list(self.path.iterdir()),[alias])
    def test_existing_final_symlink_untouched(self):
        target=self.path/'original';target.write_bytes(b'prior');link=self.path/self.pin['filename'];link.symlink_to(target)
        with self.assertRaises(helper.Refusal):self.fetch()
        self.assertTrue(link.is_symlink());self.assertEqual(target.read_bytes(),b'prior')
    def test_raced_publication_never_overwrites_other_file(self):
        model=self.path/self.pin['filename'];original=helper.os.link
        def race(source,target,**kwargs):model.write_bytes(b'raced');return original(source,target,**kwargs)
        with patch.object(helper.os,'link',race):
            with self.assertRaises(helper.Refusal):self.fetch()
        self.assertEqual(model.read_bytes(),b'raced');self.assertFalse((self.path/'.model-download').exists());self.assertFalse((self.path/'MODEL-INPUT.json').exists())
    def test_wrong_directory_mode_refused(self):
        self.path.chmod(0o755)
        with self.assertRaises(helper.Refusal):self.fetch()
        self.assertFalse(list(self.path.iterdir()))
    def test_http_and_credential_url_refused_before_request(self):
        for url in ('http://publisher.invalid/x','https://user:secret@publisher.invalid/x'):
            opener=Opener()
            with self.assertRaises(helper.Refusal):self.fetch(pin=dict(self.pin,url=url),opener=opener)
            self.assertEqual(opener.calls,0)
        self.assertFalse(list(self.path.iterdir()))
    def test_redirect_downgrade_and_credentials_refused(self):
        handler=helper.HTTPSRedirects();request=helper.urllib.request.Request('https://publisher.invalid/x')
        for url in ('http://publisher.invalid/x','https://user:secret@publisher.invalid/x'):
            with self.assertRaises(helper.Refusal):handler.redirect_request(request,None,302,'found',{},url)
        self.assertFalse(handler.hosts)
    def test_redirect_bound(self):
        handler=helper.HTTPSRedirects();request=helper.urllib.request.Request('https://publisher.invalid/x')
        for number in range(3):self.assertIsNotNone(handler.redirect_request(request,None,302,'found',{},'https://cdn.invalid/'+str(number)))
        with self.assertRaises(helper.Refusal):handler.redirect_request(request,None,302,'found',{},'https://cdn.invalid/last')
        self.assertEqual(len(handler.hosts),3)
    def test_malformed_pin_refused_without_artifacts(self):
        for pin in (dict(self.pin,bytes=True),dict(self.pin,sha256='z'*64),dict(self.pin,filename='../escape'),dict(self.pin,extra=1)):
            with self.assertRaises(helper.Refusal):self.fetch(pin=pin)
        self.assertFalse(list(self.path.iterdir()))


def main():
    global ROOT
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args();ROOT=args.output_dir
    if sys.platform!='linux' or not sys.dont_write_bytecode:raise SystemExit('Inert Linux Python-B fixtures only')
    fd=helper.directory(ROOT);os.close(fd)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FixedInput);count=suite.countTestCases()
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report=dict(status='PASS_INERT_FIXTURES_ONLY' if result.wasSuccessful() and not result.skipped else 'FAILED',tests=count,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),network=False,model_execution=False)
    fd=helper.directory(ROOT)
    try:helper.metadata(fd,'FIXTURES.json',report)
    finally:os.close(fd)
    print(json.dumps(report),flush=True)
    return 0 if result.wasSuccessful() and not result.skipped else 1


if __name__=='__main__':raise SystemExit(main())
