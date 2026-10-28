# Arafat Assistant

The portfolio distributes the assistant through `site/assistant/`; GitHub Actions
builds the Windows application. The companion runs on the user's Windows PC and
accepts typed or recorded instructions in English, Bangla and other model-supported
languages. Website and Windows app actions are reviewed in the desktop app.

The public page does not collect instructions, connect to a desktop, or request API
keys. Task data and credentials are not stored in this repository. The companion
uses the user's separately billed OpenAI API account and needs internet access.

## Windows download

A successful build on `main` publishes an `assistant-v0.2.*` preview release with
`ArafatAssistant-Windows-x64.zip` and its SHA-256 checksum. The download page finds
the newest matching assistant release and shows a link. Until one exists it shows
the build status and directs visitors to the workflow. It must not claim a running
assistant or pretend that a missing download is available.

Extract the ZIP, keep the executable and `_internal` folder together, and open
`ArafatAssistant.exe`. Python and Chromium are bundled. Enter an API key in Settings
and test typed instructions before recording. See the included `QUICK_START.txt`.

## Build and checks

On 64-bit Windows with Python 3.12, from the repository root:

```bat
python -m pip install -r assistant/requirements-build.txt
python assistant/build_windows.py
```

The build installs Chromium, runs the source tests, creates a PyInstaller one-folder
bundle, and runs the packaged executable's `--smoke-test` mode. That mode checks
frozen imports, a local Bangla browser fixture, the actual Tk interface and clean
shutdown. It makes no OpenAI requests and loads no saved API key. Only passing
builds are packaged and released. PR builds retain artifacts but do not publish a
release. No self-hosted runner is installed on the user's personal computer.

Source-only core checks, without Windows dependencies:

```text
python -m unittest discover -s assistant/desktop/tests -p test_core.py -v
```

## Limits

GitHub Pages serves the download page. It does not execute Python or control the
user's computer. This first GitHub integration is a distribution route; remote web
commands, a private command dashboard, always-on listening, automatic desktop
installation, and unattended account actions are not implemented.

The app records only after Record voice is selected, and transcripts are reviewed
before execution. Standard accessible Windows controls are supported; individual
apps may need adapters. The API key is entered locally, optionally saved through
Windows Credential Manager, and never committed to GitHub. Existing desktop
source instructions and its detailed privacy notes are in `desktop/README.txt`.

The packaged smoke checks do not validate live AI judgement, microphone capture,
or third-party app actions. Those require a first local trial. The build is an
unsigned preview, and it does not provide universal autonomous computer control.

## References

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [GitHub Actions Python builds](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [PyInstaller](https://pyinstaller.org/en/stable/)
- [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use)
