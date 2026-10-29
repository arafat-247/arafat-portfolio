"""Windows CI: verify the actual approved adapter against a disposable Notepad."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from automation import Tools


@unittest.skipUnless(sys.platform == "win32", "Requires a Windows desktop")
class WindowsLocalTests(unittest.TestCase):
    def test_notepad_launch_read_and_bangla_fill_use_observed_controls(self):
        children = []
        original = subprocess.Popen
        def launch(*args, **kwargs):
            process = original(*args, **kwargs)
            children.append(process)
            return process
        with tempfile.TemporaryDirectory() as folder:
            approvals = []
            tools = Tools(Path(folder), Path(folder) / "notes", {"notepad": str(Path(os.environ["SystemRoot"]) / "System32" / "notepad.exe")},
                          lambda *args: approvals.append(args) or True, lambda *args: None)
            tools.desktop_enabled = True
            tools.context_destination = "the local model on this PC"
            try:
                with patch("automation.subprocess.Popen", side_effect=launch):
                    tools.execute("app_open", {"alias": "notepad"})
                deadline = time.monotonic() + 15
                target = None
                while time.monotonic() < deadline:
                    target = next((row for row in tools.execute("windows_list", {})["windows"] if "Notepad" in row["title"]), None)
                    if target:
                        break
                    time.sleep(0.2)
                self.assertIsNotNone(target, "Notepad did not create a visible window")
                handle = target["handle"]
                snapshot = tools.execute("window_read", {"handle": handle})
                edit = next(row for row in snapshot["controls"] if row["type"] == "Edit")
                text = "Hello, Arafat. বাংলা পরীক্ষা।"
                tools.execute("window_fill", {"handle": handle, "control_id": edit["id"], "text": text})
                snapshot = tools.execute("window_read", {"handle": handle})
                self.assertTrue(any(text in row["text"] for row in snapshot["controls"]))
                self.assertTrue(any("local model on this PC" in detail for _, detail in approvals))
                self.assertFalse(any("sent to OpenAI" in detail for _, detail in approvals))
            finally:
                for child in children:
                    if child.poll() is None:
                        child.terminate()
                        child.wait(timeout=5)
                tools.close()


if __name__ == "__main__":
    unittest.main()
