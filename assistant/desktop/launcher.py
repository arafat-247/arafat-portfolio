"""Entry point for the portable Windows build; no API calls during smoke tests."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback
from runtime import external_program_environment, single_instance, stop_playwright


def configure_browser():
    if getattr(sys, "frozen", False):
        os.environ["ARAFAT_BROWSER_CHANNEL"] = "msedge"


def smoke_test(report_path):
    """Exercise frozen imports, Chromium, Unicode and the real app interface."""
    result = {"ok": False, "checks": [], "live_api_tested": False,
              "microphone_capture_tested": False, "windows_app_actions_tested": False}
    import threading
    report_lock = threading.RLock()
    def phase(name):
        with report_lock:
            result["stage"] = name
            Path(report_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        if sys.stdout:
            print("Packaged check: " + name, flush=True)
    def driver_observation(value):
        with report_lock:
            result["driver_diagnostic"] = value
            phase(value["stage"])
    try:
        phase("import microphone module")
        import sounddevice
        phase("import Windows automation modules")
        import pythoncom
        import pywinauto
        from keyring.backends.Windows import WinVaultKeyring
        result["checks"].append("Windows, microphone and credential modules import")
        phase("import local speech and sign-in modules")
        import faster_whisper
        import ctranslate2
        import onnxruntime
        import jwt
        import win32crypt
        # Exercise real bundled cryptography and Windows protected storage.
        from cryptography.hazmat.primitives.asymmetric import rsa
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        encoded = jwt.encode({"test": "বাংলা"}, key, algorithm="RS256")
        assert jwt.decode(encoded, key.public_key(), algorithms=["RS256"])["test"] == "বাংলা"
        from chatgpt_auth import ProtectedStore
        with tempfile.TemporaryDirectory(prefix="assistant-auth-check-") as folder:
            store = ProtectedStore(Path(folder))
            store.save({"test": "local-only"})
            assert store.load() == {"test": "local-only"}
            store.delete()
        result["checks"].append("Local speech imports, signed-token verification and Windows protected storage work")
        def browser_probe():
            try:
                phase("start browser driver")
                from browser_driver import start_playwright
                with external_program_environment():
                    p = start_playwright()
                    try:
                        phase("launch Microsoft Edge")
                        browser = p.chromium.launch(headless=True, channel="msedge", timeout=20_000)
                        phase("Microsoft Edge started")
                        page = browser.new_page()
                        page.set_default_timeout(5000)
                        phase("test page created")
                        page.set_content('<html lang="bn"><body><input aria-label="নির্দেশ"><button>শুরু</button></body></html>')
                        field = page.get_by_role("textbox", name="নির্দেশ")
                        field.fill("বাংলা পরীক্ষা")
                        assert field.input_value() == "বাংলা পরীক্ষা"
                        assert page.get_by_role("button", name="শুরু").count() == 1
                        phase("Bangla browser input verified")
                        browser.close()
                        phase("Microsoft Edge closed")
                    finally:
                        import faulthandler
                        trace = Path(str(report_path) + ".trace.txt").open("w", encoding="utf-8")
                        faulthandler.dump_traceback_later(15, repeat=True, file=trace)
                        try:
                            result["driver_cleanup_forced"] = stop_playwright(p, observe=driver_observation)
                        finally:
                            faulthandler.cancel_dump_traceback_later()
                            trace.close()
                phase("browser driver closed")
                result["checks"].append("Installed Microsoft Edge launches and handles Bangla input")
            except Exception:
                result["browser_error"] = traceback.format_exc()

        browser_worker = threading.Thread(target=browser_probe, name="assistant-browser-check", daemon=True)
        browser_worker.start()
        browser_worker.join(timeout=45)
        if browser_worker.is_alive():
            raise RuntimeError("The packaged browser worker did not close cleanly within 45 seconds.")
        if result.get("browser_error"):
            raise RuntimeError(result["browser_error"])
        phase("open desktop interface")
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
                root.update()
                from PIL import ImageGrab
                def capture(label):
                    root.update()
                    ImageGrab.grab().save(str(report_path) + "." + label + ".png")
                def visible(widget, window):
                    assert widget.winfo_ismapped(), "A required control is not visible"
                    top = widget.winfo_rooty()
                    bottom = top + widget.winfo_height()
                    assert window.winfo_rooty() <= top < bottom <= window.winfo_rooty() + window.winfo_height(), "A required control falls below its window"
                    assert bottom < window.winfo_screenheight(), "A required control falls below the screen"
                assert application.config["auth_mode"] == "local"
                for control in (application.input, application.record_button, application.run_button, application.stop_button):
                    visible(control, root)
                capture("main")
                application.show_local_setup()
                root.update()
                capture("local-setup")
                for child in root.winfo_children():
                    if isinstance(child, tk.Toplevel):
                        child.destroy()
                application.show_settings()
                root.update()
                for child in root.winfo_children():
                    if isinstance(child, tk.Toplevel):
                        for row in child.winfo_children():
                            for control in row.winfo_children():
                                if isinstance(control, app.ttk.Button) and control.cget("text") == "Save settings":
                                    visible(control, child)
                capture("settings")
                for child in root.winfo_children():
                    if isinstance(child, tk.Toplevel):
                        child.destroy()
                assert application.input.winfo_exists()
                application.input.insert("1.0", "বাংলায় নির্দেশ")
                assert application.input.get("1.0", "end").strip() == "বাংলায় নির্দেশ"
                root.after(100, application.close)
                root.after(10_000, root.quit)
                root.mainloop()
                application.worker.join(timeout=2)
                if application.worker.is_alive():
                    raise RuntimeError("The application did not close cleanly.")
        result["checks"].append("Desktop interface defaults to local mode, keeps instruction/run/settings controls on screen, accepts Bangla text and closes")
        result["ok"] = True
        phase("complete")
    except Exception:
        result["error"] = traceback.format_exc()
    Path(report_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if result["ok"] else 1


def main():
    configure_browser()
    if sys.argv[1:] == ["--local"]:
        os.environ["ARAFAT_START_LOCAL"] = "1"
    if len(sys.argv) == 3 and sys.argv[1] == "--smoke-test":
        return smoke_test(sys.argv[2])
    try:
        from app import main as run_application
        import settings
        with single_instance(settings.data_directory()) as allowed:
            if not allowed:
                import ctypes
                ctypes.windll.user32.MessageBoxW(None, "Arafat Assistant is already running. Close its other window before starting a second copy.", "Arafat Assistant", 0x40)
                return 0
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
    from multiprocessing import freeze_support
    freeze_support()
    raise SystemExit(main())
