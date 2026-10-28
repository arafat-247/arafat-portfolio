import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

DESKTOP = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(DESKTOP))
import launcher

spec = importlib.util.spec_from_file_location("assistant_build_windows", DESKTOP.parent / "build_windows.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PackagingTests(unittest.TestCase):
    def test_portable_archive_preserves_support_files_and_checksum(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            bundle=folder/'app'
            (bundle/'_internal').mkdir(parents=True)
            (bundle/'ArafatAssistant.exe').write_bytes(b'build-fixture')
            (bundle/'_internal'/'required.dll').write_bytes(b'required-support-file')
            archive=builder.package_app(bundle,folder/'release')
            with zipfile.ZipFile(archive) as z:
                self.assertEqual(z.read('ArafatAssistant/_internal/required.dll'),b'required-support-file')
            digest=hashlib.sha256(archive.read_bytes()).hexdigest()
            self.assertTrue(archive.with_suffix('.zip.sha256').read_text().startswith(digest+'  '))

    def test_packaged_app_selects_installed_edge(self):
        with patch.object(sys,'frozen',True,create=True),patch.dict(os.environ,clear=False):
            launcher.configure_browser()
            self.assertEqual(os.environ['ARAFAT_BROWSER_CHANNEL'],'msedge')


if __name__ == '__main__':
    unittest.main()
