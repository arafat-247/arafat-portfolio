ARAFAT ASSISTANT — WINDOWS STARTER 0.1
Prepared 28 October 2026

A desktop assistant for typed and recorded instructions. Designed for English,
Bangla, romanised Bangla and other languages understood by the selected models.
It can use its own browser and basic accessible controls in Windows apps.

THIS DOWNLOAD

This is a Python source package with Windows setup and launch scripts. It is
not a compiled or signed .exe installer. You can inspect and change its code.
Intended target: Windows 10/11, 64-bit, with Python 3.12 or 3.11 installed.

QUICK START

1. Extract the whole ZIP into a folder you can write to, such as a folder inside
   your Downloads directory. Do not run it from inside the ZIP.
2. Install 64-bit Python 3.12 if needed:
   https://www.python.org/downloads/windows/
   Include Tcl/Tk and the Python launcher in the installation.
3. Double-click setup.cmd. It creates a local Python environment and installs
   the required packages and Chromium. Internet access is needed. Setup may
   take several minutes. You do not need to run it as administrator.
4. When setup finishes, double-click start.cmd.
5. Select Settings. Paste your OpenAI API key in its masked field and save.
   Create or manage a key at https://platform.openai.com/api-keys
   API setup guidance: https://developers.openai.com/api/docs/quickstart
6. Type an instruction and select Run instruction, or use Record voice.

This app uses the separately billed OpenAI API. It does not use your ChatGPT
website session or draw usage from a ChatGPT subscription. You need access to
the models in Settings and an API account with available quota. Charges depend
on your usage. Check billing and set suitable account limits before live use:
https://developers.openai.com/api/docs/pricing
https://platform.openai.com/settings/organization/billing/overview

VOICE AND LANGUAGES

Select a speech language, or leave Auto-detect selected. English + Bangla sends
both language hints. Select Record voice, speak, then Stop recording. Recordings
are limited to 60 seconds. They are transcribed after recording stops.

Review and edit the transcript, then select Run instruction. Transcription NEVER
automatically starts a task. Stop task while recording discards the recording.
This version has no wake word, always-on listening or spoken replies.

Try:
  Open https://www.thedailystar.net and tell me its main visible headlines.
  https://www.thedailystar.net খুলে প্রধান শিরোনামগুলো বাংলায় বলো।
  একটি নতুন ফাইলে লিখে রাখো: আজকের কাজের তালিকা।
  Open Notepad and enter: This is my first assistant test.

Language recognition is model-dependent. This starter offers language hints;
it does not promise support for every language, dialect or mixed-language
utterance. It has not been evaluated with a Bangla audio test set. Correct
names, numbers and ambiguous wording in the transcript before executing.
The selected transcription model supports multilingual input and multiple
language hints. Its documentation explains the accepted hint formats:
https://developers.openai.com/api/docs/guides/speech-to-text
https://developers.openai.com/api/docs/models/gpt-transcribe

BROWSER TASKS

The assistant opens a separate, visible Chromium browser. Your normal Edge or
Chrome tabs and existing sign-ins are not imported. If a task needs login,
sign in yourself in the assistant browser. Enter passwords and authentication
codes manually. Keep the browser open, then ask the assistant to continue.

The implemented tools can open public HTTP(S) pages, read visible text and
controls, switch tabs, click, fill text fields and choose dropdown options.
Each page read is limited to 18,000 text characters and 120 controls. The agent
has a limit of 18 model rounds and 24 tool calls per instruction.

Website navigation and changes appear in a local review window. Select Allow
once to perform the displayed action, or Decline and stop to end the task.
Read the current page as well as the review text before allowing a click.

This starter does not implement file upload/download, CAPTCHA handling,
paywall bypass, iframe navigation or visual control of canvas-only interfaces.
Some complex or protected sites will need an additional adapter. Public URL
validation blocks explicit local/private addresses, but it is not a firewall
or a guarantee against DNS-based redirection. Run it in your normal user
account and choose sites you intend to use.

Browser automation uses Playwright:
https://playwright.dev/python/docs/intro
https://playwright.dev/python/docs/locators

WINDOWS APPS

Enable Allow Windows app access this session to use app tools. It starts off
each time you launch the assistant. The default launch aliases are notepad,
calculator and paint. If an app is missing, update its path in Settings.

Add another application as an alias and an absolute .exe path, for example:
  myapp=C:\Program Files\MyApp\MyApp.exe
Do not include command arguments. The model cannot choose arbitrary programs
to launch; it can only launch the aliases you have configured.

The app tools list visible window titles, read a window's accessibility tree,
click an observed control and replace text in a standard Edit control. Reads
and changes need approval. Window reads omit controls marked as passwords.
Each window read is limited to 160 controls and 24,000 text characters.
Custom-drawn editors, some modern Notepad versions, elevated windows, complex
menus and applications without suitable accessibility controls may not work.
This is basic UI Automation support, not universal control of every app.

Windows app automation uses pywinauto's UIA backend:
https://pywinauto.readthedocs.io/en/latest/getting_started.html
https://pywinauto.readthedocs.io/en/latest/code/pywinauto.controls.uia_controls.html

FILES, PRIVACY AND CONTROLS

The Save note tool creates UTF-8 .txt files in Documents\ArafatAssistant. Select
Saved notes to open that folder. Existing files are never overwritten by this
tool. It cannot read, move or delete arbitrary files. Word/PDF export is not
implemented in this version.

Instructions, recent conversation context, recorded audio submitted for
transcription, and selected website/app text are sent to the OpenAI API.
Browser interaction also sends data to the websites you visit. The API key
is sent only in the request authorisation header, not in the model prompt.
The app requests store=false for Responses API calls. This does not make
requests offline or override OpenAI's API data policies:
https://developers.openai.com/api/docs/guides/your-data

The app keeps its conversation and recorded audio in memory; it does not
deliberately save them as local history. Text you ask it to save is written
to the output folder. The browser profile persists cookies and sign-ins in
%LOCALAPPDATA%\ArafatAssistant\browser-profile. Browser-managed storage may
retain visited content. Close the assistant before clearing that profile.

Settings are in %LOCALAPPDATA%\ArafatAssistant\settings.json. The API key is
never written in that JSON file. By default it is held for the session. If
you select Remember key, it is saved using Windows Credential Manager via
the keyring Windows backend. Clear the checkbox and save to remove that saved
credential. OPENAI_API_KEY is also accepted when set before app launch.
https://keyring.readthedocs.io/en/latest/

The model is instructed to treat website and app text as untrusted data.
Local approvals provide human review; model instructions do not eliminate
prompt-injection risk. For publishing, sending or payments, review the exact
destination and final content yourself. The starter has no autonomous shell
or software-installation tool.

Stop task takes effect between operations. An API request can take up to its
60-second timeout; browser operations have their own shorter timeouts. Stop
cannot recall a sent message, undo a click or remove an already saved file.
Declining an approval ends the task. Closing waits for the current operation
before shutting down the browser. New conversation clears model context and
the visible activity log; it keeps browser tabs and sign-ins.

MODELS AND CHANGES

Default task model: gpt-5.4-mini
Default speech-to-text model: gpt-transcribe
The names are editable in Settings. Access depends on your API account. A
replacement task model must support Responses, function calls and the request
options in core.py. A different transcription model may need an adapter.
There is no automatic fallback that silently changes models or cost.
https://developers.openai.com/api/docs/models/gpt-5.4-mini
https://developers.openai.com/api/docs/guides/function-calling

TESTING STATUS

Automated core checks cover Unicode handling, file creation without overwrite,
URL restrictions, transcription request formatting, refusal/cancellation and
the bounded model loop. The included browser checks use an in-memory fixture
with Bangla controls. Tests simulate model responses; they do not prove how
well a live model chooses actions.

Development results: core checks passed. The real-browser tests were skipped
because both Chromium download attempts returned invalid archives in this
environment. Browser actions therefore remain unverified here; check.cmd will
attempt them after a successful installation on your computer.

This package was produced in a Linux environment. Windows GUI operation,
microphone capture, Credential Manager, Windows app control and live OpenAI
requests were NOT tested on your computer. No API key was supplied, and no
live API requests were made during development.

Run check.cmd after setup. It checks installation and runs the local tests.
Use one simple, non-sensitive task as your first Windows test. If anything
fails, copy the visible error message, without including an API key.

TROUBLESHOOTING

No Python: install 64-bit Python 3.12 with Tcl/Tk and its launcher, then retry.
No Chromium: run setup.cmd again. Close other copies of the assistant.
No microphone: check Windows Settings > Privacy & security > Microphone and
the default input device. Typed instructions remain available.
API 401: check the key in Settings.
API 429: check billing, remaining quota and rate limits.
Model/language error: confirm account access and model settings. For language
hint errors, try Auto-detect. This does not guarantee language recognition.
No usable app controls: explain the app and task when requesting an adapter.
No visible browser output: ask it to read again after the page finishes loading.

SOURCE MAP

app.py          Desktop interface, task queue and approval windows
core.py         API transport, tool schemas and model loop
automation.py   Browser and Windows app adapters; note saving
voice.py        Bounded microphone recording and WAV creation
settings.py     Preferences and optional Windows credential storage
selftest.py     Local installation checks; no OpenAI requests
tests/          Automated checks
requirements.txt  Required third-party packages
setup.cmd       Install dependencies
start.cmd       Launch the app
check.cmd       Run checks

This starter is ready for an initial Windows trial after setup. It is not a
claim of production readiness or general reliability on arbitrary websites
and apps. Source references were checked on 28 October 2026.
