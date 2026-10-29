"""Build a portable x64 app on Windows; use installed Microsoft Edge."""
from __future__ import annotations
import hashlib
import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
DESKTOP = ROOT / "desktop"
OUTPUT = ROOT / "release"
NAME = "ArafatAssistant"

QUICK_START = """ARAFAT ASSISTANT — PORTABLE WINDOWS PREVIEW

1. Extract the entire ZIP into a folder you can write to.
2. Keep ArafatAssistant.exe and its _internal folder together.
3. Open ArafatAssistant.exe. Python is included; Microsoft Edge must be installed.
4. Open Start Local Assistant.cmd to explicitly choose local mode, including on an older installation.
5. Open Local setup. Select Download Ollama and finish its official Windows installer.
6. Return to Local setup. Choose Standard (about 2.5 GB) or Light (about 1.4 GB),
   then select Download selected model. The app starts its own local engine.
7. Choose Task model and test a short typed instruction. No OpenAI sign-in or API credit is used.
8. Try Record voice. First use downloads a multilingual local speech model.
9. Review the transcript before selecting Run instruction.
10. Enable Windows app access in the app for desktop tasks. Start with Open Notepad.

Local mode uses a downloaded model on your PC with Ollama cloud features off.
The Light model uses less memory; Standard may follow instructions better.
Model download size is not the total RAM needed. Speed and quality depend on
your CPU, graphics hardware, memory and task. Begin with short tasks.
First-time model downloads and websites need internet. Local inference does not.

This is an unsigned preview. Windows SmartScreen may show More info / Run anyway.
Only continue if you downloaded the app from the repository above and trust it.
Keep Windows security protections enabled.
ChatGPT mode uses your existing Plus / Pro plan allowance, subject to eligibility
and usage limits. No API credit is required in that mode. Optional API mode is
billed separately and must be selected explicitly; there is no automatic fallback.
Speech is transcribed on your PC. First voice use downloads several hundred MB
from Hugging Face. Instructions, reviewed transcripts and selected website/app
text stay on this PC in Local mode and go to OpenAI in ChatGPT/API modes.
The portfolio distributes the app; it does not control your PC.
Browser sign-ins happen manually in the assistant's own browser. Microphone
capture, live model behaviour and your installed app controls need local tests.
Stop takes effect between operations and cannot undo completed actions.

Build details: BUILD_INFO.json
Packaged checks: SMOKE_TEST.json
Source and build history: https://github.com/arafat-247/arafat-portfolio
"""


def run(*arguments, cwd=DESKTOP, env=None, timeout=None):
    subprocess.run([str(value) for value in arguments], cwd=cwd, env=env, check=True, timeout=timeout)


def package_app(bundle: Path, output: Path) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    archive = output / "ArafatAssistant-Windows-x64.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(bundle.rglob("*")):
            if path.is_file():
                z.write(path, Path(NAME) / path.relative_to(bundle))
    with archive.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    archive.with_suffix(archive.suffix + ".sha256").write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    return archive


def main():
    if sys.platform != "win32" or platform.architecture()[0] != "64bit":
        raise SystemExit("Build this package on 64-bit Windows with Python 3.12.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["check", "freeze", "smoke", "package"])
    stage = parser.parse_args().stage
    environment = dict(os.environ, ARAFAT_BROWSER_CHANNEL="msedge")
    if stage in (None, "check"):
        run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v", env=environment)
        if stage:
            return
    if stage in (None, "freeze"):
        freeze(environment)
        if stage:
            return
    bundle = ROOT / "dist" / NAME
    report = bundle / "SMOKE_TEST.json"
    if stage in (None, "smoke"):
        run(bundle / f"{NAME}.exe", "--smoke-test", report, env=environment, timeout=90)
        smoke = json.loads(report.read_text(encoding="utf-8"))
        if not smoke.get("ok"):
            raise SystemExit("Packaged application smoke test failed.")
        if stage:
            return
    if not json.loads(report.read_text(encoding="utf-8")).get("ok"):
        raise SystemExit("A passing packaged smoke test is required before packaging.")
    (bundle / "QUICK_START.txt").write_text(QUICK_START, encoding="utf-8")
    (bundle / "Start Local Assistant.cmd").write_text('@echo off\r\nstart "" "%~dp0ArafatAssistant.exe" --local\r\n', encoding="ascii")
    shutil.copyfile(ROOT / "LICENSE", bundle / "LICENSE.txt")
    (bundle / "BUILD_INFO.json").write_text(json.dumps({
        "source_commit": os.environ.get("GITHUB_SHA", "local-build"),
        "python": platform.python_version(), "platform": platform.platform(),
        "build_kind": "unsigned Windows x64 portable preview", "smoke_test_passed": True,
        "browser": "installed Microsoft Edge", "live_api_tested": False,
        "microphone_capture_tested": False, "windows_app_actions_tested": True,
        "windows_app_fixture": "Disposable Notepad English/Bangla read/fill in source tests",
        "local_protocol_tested": True, "local_model_engine": "Ollama, own loopback process, OLLAMA_NO_CLOUD=1",
        "chatgpt_live_sign_in_tested": False, "local_speech_model_tested": False,
    }, indent=2), encoding="utf-8")
    archive = package_app(bundle, OUTPUT)
    print(f"Created {archive}")


def freeze(environment):
    run(sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--windowed",
        "--name", NAME, "--distpath", ROOT / "dist", "--workpath", ROOT / "build",
        "--specpath", ROOT, "--collect-all", "playwright", "--collect-all", "sounddevice",
        "--collect-all", "pywinauto", "--collect-all", "comtypes",
        "--collect-all", "faster_whisper", "--collect-all", "ctranslate2",
        "--collect-all", "av", "--collect-all", "onnxruntime", "--collect-all", "tokenizers",
        "--collect-submodules", "jwt", "--copy-metadata", "faster-whisper",
        "--collect-submodules", "keyring.backends.Windows", "--hidden-import", "win32timezone",
        "--hidden-import", "unittest.mock",
        DESKTOP / "launcher.py", env=environment)


if __name__ == "__main__":
    main()
