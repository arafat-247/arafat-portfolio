"""Run after installation. Does not inspect your apps or call OpenAI."""
import importlib
import platform
import sys


def main():
    print("Arafat Assistant local installation check")
    print("System:", platform.system(), platform.machine())
    print("Python:", platform.python_version())
    problems = []
    modules = ["tkinter", "sounddevice", "playwright.sync_api"]
    if sys.platform == "win32":
        modules += ["pywinauto", "pythoncom", "keyring.backends.Windows"]
    for module in modules:
        try:
            importlib.import_module(module)
            print("OK:", module)
        except Exception as exc:
            problems.append(f"{module}: {exc}")
    try:
        import tkinter as tk
        print("Tcl:", tk.Tcl().eval("info patchlevel"))
    except Exception as exc:
        problems.append(f"Tcl: {exc}")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content('<html lang="bn"><body><button>শুরু করুন</button></body></html>')
            assert page.get_by_role("button", name="শুরু করুন").count() == 1
            browser.close()
            print("OK: Chromium starts and recognises Bangla page text")
    except Exception as exc:
        problems.append(f"Chromium: {exc}")
    try:
        import sounddevice as sd
        device = sd.query_devices(kind="input")
        print("Microphone:", device["name"])
    except Exception:
        print("NOTE: No default microphone found. Text still works; configure a microphone before recording.")
    if problems:
        for problem in problems:
            print("FAILED:", problem)
        print("Run setup.cmd again after correcting the errors.")
        return 1
    print("Installation check passed. No OpenAI request was made.")
    print("Microphone capture, live transcription and Windows app actions still need a real task test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
