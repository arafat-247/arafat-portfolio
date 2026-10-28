"""Build a portable x64 app on Windows, with its own Python and Chromium."""
from __future__ import annotations
import hashlib
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
3. Open ArafatAssistant.exe. Python and Chromium are included.
4. In Settings, enter your own OpenAI API key and save.
5. Test a short typed instruction, then try Record voice.
6. Review the transcript before selecting Run instruction.
7. Enable Windows app access in the app for desktop tasks.

This is a preview build. It requires internet and separately billed API usage.
Your instructions, submitted recordings and selected website/app text go to
OpenAI. The portfolio website distributes the app; it does not control your PC.
Browser sign-ins happen manually in the assistant's own browser. Microphone
capture, live model behaviour and your installed app controls need local tests.
Stop takes effect between operations and cannot undo completed actions.

Build details: BUILD_INFO.json
Packaged checks: SMOKE_TEST.json
Source and build history: https://github.com/arafat-247/arafat-portfolio
"""


def run(*arguments, cwd=DESKTOP, env=None):
    subprocess.run([str(value) for value in arguments], cwd=cwd, env=env, check=True)


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
    browsers = ROOT / "browsers"
    environment = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=str(browsers))
    run(sys.executable, "-m", "playwright", "install", "chromium", env=environment)
    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v", env=environment)
    run(sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--windowed",
        "--name", NAME, "--distpath", ROOT / "dist", "--workpath", ROOT / "build",
        "--specpath", ROOT, "--collect-all", "playwright", "--collect-all", "sounddevice",
        "--collect-all", "pywinauto", "--collect-all", "comtypes",
        "--collect-submodules", "keyring.backends.Windows", "--hidden-import", "win32timezone",
        "--hidden-import", "unittest.mock", "--add-data", str(browsers) + os.pathsep + "browser-binaries",
        DESKTOP / "launcher.py", env=environment)
    bundle = ROOT / "dist" / NAME
    report = bundle / "SMOKE_TEST.json"
    # Capture a missing-dependency or frozen-driver failure before distributing.
    run(bundle / f"{NAME}.exe", "--smoke-test", report, env=environment)
    smoke = json.loads(report.read_text(encoding="utf-8"))
    if not smoke.get("ok"):
        raise SystemExit("Packaged application smoke test failed.")
    (bundle / "QUICK_START.txt").write_text(QUICK_START, encoding="utf-8")
    (bundle / "BUILD_INFO.json").write_text(json.dumps({
        "source_commit": os.environ.get("GITHUB_SHA", "local-build"),
        "python": platform.python_version(), "platform": platform.platform(),
        "build_kind": "unsigned Windows x64 portable preview", "smoke_test_passed": True,
        "live_api_tested": False, "microphone_capture_tested": False,
        "windows_app_actions_tested": False,
    }, indent=2), encoding="utf-8")
    archive = package_app(bundle, OUTPUT)
    print(f"Created {archive}")


if __name__ == "__main__":
    main()
