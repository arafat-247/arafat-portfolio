# Arafat Assistant

A portable Windows companion for typed and recorded instructions, websites and
supported Windows app controls. The portfolio is a download page; work runs in
the desktop companion on the user's PC.

## Use an existing ChatGPT Plus or Pro plan

1. Download the newest `assistant-v0.3.*` Windows preview from the repository's
   Releases page or https://arafatrahaman.com/assistant/.
2. Close the older assistant, extract the whole ZIP into a new folder, and open
   `ArafatAssistant.exe`. Keep `_internal` beside it. Python is included;
   Microsoft Edge must be installed.
3. Select **Continue with ChatGPT**. In your browser, sign in with your eligible
   personal Plus or Pro account and allow **Use your ChatGPT plan**.
4. Return to the app and choose an available ChatGPT model. The choices come
   from the signed-in account; no API key is required in ChatGPT mode.
5. Type `Reply in Bangla and explain what you can do`, then select
   **Run instruction**. Approve only the proposed actions you want performed.
6. Try `Open https://example.com and summarise the page in Bangla`.
7. To use desktop controls, enable **Allow Windows app access this session**.
   Start with `Open Notepad`.

ChatGPT mode uses the existing plan allowance, including any app-specific cap.
It does not provide unlimited access or a separate allowance. **Manage usage**
opens ChatGPT usage settings. If the direct settings link does not open that
panel, use ChatGPT Settings → Usage. Eligibility and model availability are
controlled by OpenAI. This app does not charge an additional fee in ChatGPT mode.

**Optional API mode** in Settings uses a separately billed OpenAI Platform
account. An API key alone does not add API credit, and a Plus subscription does
not fund API-key requests. API mode must be selected explicitly. The app never
switches to it automatically when ChatGPT sign-in or a plan limit fails.
Existing 0.2 preferences migrate to ChatGPT mode by default.

## Voice without transcription API charges

Select **Record voice** and approve preparing local speech recognition. Speak,
select **Stop recording**, review or edit the transcript, then select
**Run instruction**. Nothing runs just because recording has stopped.

The app bundles faster-whisper's inference runtime. On first voice use it
downloads the public multilingual `small` model from Hugging Face (several
hundred MB) into the app's local data folder. Loading and transcription use the
CPU and may take time. Later recordings reuse the model. Audio is processed on
the PC, not sent to a transcription API. English and Bangla language hints are
available; mixed speech uses automatic detection. Recognition can make mistakes,
so review the text before running it. There is no always-on listening or spoken
reply feature. Recordings are bounded to 60 seconds.

## Windows security prompt

This is an unsigned preview. SmartScreen may show **Windows protected your PC**.
If you downloaded this specific app from this repository and trust the source,
select **More info**, check the app name, then **Run anyway** if offered. Keep
Defender and SmartScreen enabled. A managed computer may prevent running it.

## Accounts and privacy

Sign-in uses OpenAI's documented public-client OAuth flow with a temporary
127.0.0.1 callback, fresh state/nonce/PKCE, signed identity validation and explicit
ChatGPT-plan permission. It does not read browser cookies or reuse another app's
credentials. Tokens are encrypted for the current Windows user with DPAPI.
Credentials, recordings and instructions are never committed to GitHub.

Settings lets users reconnect a saved registration or add another ChatGPT
account. Registrations are kept separate, including when email addresses match.
Changing accounts clears the current model conversation. Signing out attempts
remote refresh-token revocation, removes local tokens for that account and
retains its registration for future sign-in. If remote revocation cannot be
confirmed, the app says so; disconnect the app in ChatGPT Settings → Security
and login → Sign in with ChatGPT. Run only one companion copy at a time.

Instructions, reviewed transcripts and selected website/app text are sent to
OpenAI when a task runs. Recordings remain local and are not written to disk by
the app. The browser stores its own profile and sign-ins locally. Passwords and
website sign-ins are entered by the user. Proposed website/app changes require
local approval. Notes are saved as new UTF-8 TXT files in
Documents/ArafatAssistant, without overwriting existing notes.

## Limits and verification

This is a preview, not universal computer control. The app supports observed
browser DOM controls and standard accessible Windows controls. Some apps need
adapters. It has no arbitrary shell command tool, remote portfolio command
panel, automatic installation, wake word or unattended account actions.
Stop applies between operations and cannot undo completed work.

Build checks cover callback state and PKCE, real signed-token verification,
permission enforcement, account isolation, token rotation, complete streamed
responses, local transcription orchestration, browser controls and packaging.
The pinned Playwright driver uses directly owned native process pipes and a
reader thread, avoiding Windows asyncio subprocess-wait cleanup. Browser checks
use the companion's worker-thread architecture. Protocol checks cover real SDK
startup/shutdown, framed messages and Bangla text. The packaged check verifies
local speech imports, RSA verification, DPAPI storage, Edge with Bangla input,
and the real Tk interface opening and closing.
It makes no OpenAI request and downloads no speech model. Live sign-in, actual
speech recognition, microphone capture and individual app tasks require the
user's local trial. A passing build does not establish live account eligibility.

## Build from source

On 64-bit Windows with Python 3.12, from the repository root:

```bat
python -m pip install -r assistant/requirements-build.txt
python assistant/build_windows.py
```

Source checks: `python -m unittest discover -s assistant/desktop/tests -v`.
The Windows CI runs source checks, freezes the app, checks the packaged app,
then creates the ZIP and SHA-256 checksum. Only a passing main-branch build
publishes an `assistant-v0.3.*` preview release. Pull requests retain test
artifacts and do not publish a release.

## References

- https://developers.openai.com/siwc/quickstart
- https://developers.openai.com/siwc/token-sharing-open-source/sign-in
- https://developers.openai.com/siwc/token-sharing-open-source/profiles-and-sessions
- https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference
- https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations
- https://developers.openai.com/siwc/token-sharing-open-source/errors-and-recovery
- https://github.com/SYSTRAN/faster-whisper
- https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
