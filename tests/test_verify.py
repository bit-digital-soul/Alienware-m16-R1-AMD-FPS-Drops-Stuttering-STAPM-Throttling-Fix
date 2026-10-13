"""Refusal-path tests: malformed or foreign inputs must not be accepted."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify', ROOT / 'tools/verify.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patch = json.loads((ROOT / 'evidence/firmware-manifest.json').read_text())['patch']
        cls.config = (ROOT / cls.patch['config']).read_bytes()

    def test_packaged_config_and_evidence(self):
        verify.verify_package(ROOT)

    def test_changed_config_and_encoding_are_rejected(self):
        variants = [self.config.replace(b'Op Exec', b'Op Loaded'),
                    self.config.replace(b'\r\n', b'\n'),
                    b'\xef\xbb\xbf' + self.config,
                    self.config.replace(b'ED0932C0', b'ED0932C1')]
        for data in variants:
            with self.subTest(sha256=hashlib.sha256(data).hexdigest()):
                with self.assertRaises(verify.VerificationError):
                    verify.verify_config(data, self.patch)

    def test_foreign_pe_is_rejected_without_modification(self):
        old, new = verify.verify_config(self.config, self.patch)
        data = bytearray(verify.PE_SIZE)
        data[0x22C0:0x22C0 + len(old)] = old
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'foreign.efi'
            path.write_bytes(data)
            before = verify.digest(path)
            with self.assertRaises(verify.VerificationError):
                verify.verify_pe(path, old, new)
            self.assertEqual(before, verify.digest(path))
            self.assertEqual(len(list(Path(folder).iterdir())), 1)

    def test_checksum_paths_cannot_escape_repository(self):
        with self.assertRaises(verify.VerificationError):
            verify.within_root(ROOT, '../outside-file')

    def test_wrong_size_firmware_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'BIOS_IMG.rcv'
            path.write_bytes(b'not a recovery image')
            with self.assertRaises(verify.VerificationError):
                verify.exact_file(path, verify.BIOS_SIZE, verify.BIOS_SHA, 'BIOS')


if __name__ == '__main__':
    unittest.main()
