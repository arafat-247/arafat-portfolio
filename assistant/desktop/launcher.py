"""Entry point for the portable Windows build; no API calls during smoke tests."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback


def configure_browser():
    if getattr(sys, "frozen", False):
        os.environ["ARAFAT_BROWSER_CHANNEL"] = "msedge"


def smoke_test(report_path):
    """Exercise frozen imports, Chromium, Unicode and the real app interface."""
    result = {"ok": False, "checks": [], "live_api_tested": False,
              "microphone_capture_tested": False, "windows_app_actions_tested": False}
    try:
        import sounddevice
        import pythoncom
        import pywinauto
        from keyring.backends.Windows import WinVaultKeyring
        result["checks"].append("Windows, microphone and credential modules import")
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, channel="msedge")
            page = browser.new_page()
            page.set_content('<html lang="bn"><body><input aria-label="নির্দেশ"><button>শুরু</button></body></html>')
            field = page.get_by_role("textbox", name="নির্দেশ")
            field.fill("বাংলা পরীক্ষা")
            assert field.input_value() == "বাংলা পরীক্ষা"
            assert page.get_by_role("button", name="শুরু").count() == 1
            browser.close()
        result["checks"].append("Installed Microsoft Edge launches and handles Bangla input")
        import tkinter as tk
        import app
        with tempfile.TemporaryDirectory(prefix="assistant-smoke-") as directory:
            # The smoke test must not load a user's key or persist settings.
            from unittest.mock import patch
            with patch("app.settings.read_key", return_value=("", False)), \
                 patch("app.settings.data_directory", return_value=Path(directory)), \
                 patch("app.settings.output_directory", return_value=Path(directory) / "notes"):
                root = tk.Tk()
                application = app.Application(root)
                root.update_idletasks()
                assert application.input.winfo_exists()
                application.input.insert("1.0", "বাংলায় নির্দেশ")
                assert application.input.get("1.0", "end").strip() == "বাংলায় নির্দেশ"
                root.after(100, application.close)
                root.after(10_000, root.quit)
                root.mainloop()
                application.worker.join(timeout=2)
                if application.worker.is_alive():
                    raise RuntimeError("The application did not close cleanly.")
        result["checks"].append("Desktop interface opens, accepts Bangla text and closes")
        result["ok"] = True
    except Exception:
        result["error"] = traceback.format_exc()
    Path(report_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if result["ok"] else 1


def main():
    configure_browser()
    if len(sys.argv) == 3 and sys.argv[1] == "--smoke-test":
        return smoke_test(sys.argv[2])
    try:
        from app import main as run_application
        run_application()
        return 0
    except Exception:
        folder = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ArafatAssistant"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "startup-error.txt"
        error = traceback.format_exc()
        key = os.environ.get("OPENAI_API_KEY", "")
        if key:
            error = error.replace(key, "[key hidden]")
        path.write_text(error, encoding="utf-8")
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, f"The assistant could not start.\nDetails: {path}", "Arafat Assistant", 0x10)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
