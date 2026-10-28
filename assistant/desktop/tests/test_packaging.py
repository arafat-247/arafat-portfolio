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
from runtime import external_program_environment

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

    @unittest.skipUnless(sys.platform == 'win32', 'Windows DLL state check')
    def test_external_program_environment_restores_path_after_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = str(Path(tmp)) + os.pathsep + os.environ.get('PATH','')
            with patch.object(sys,'frozen',True,create=True),patch.object(sys,'_MEIPASS',tmp,create=True),patch.dict(os.environ,{'PATH':original}):
                with self.assertRaisesRegex(RuntimeError,'fixture failure'):
                    with external_program_environment():
                        self.assertNotIn(tmp,os.environ['PATH'].split(os.pathsep))
                        raise RuntimeError('fixture failure')
                self.assertEqual(os.environ['PATH'],original)


if __name__ == '__main__':
    unittest.main()
