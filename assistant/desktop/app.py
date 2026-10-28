"""Arafat Assistant — Windows desktop starter, version 0.1."""
from __future__ import annotations
import copy
import os
from pathlib import Path
import queue
import re
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from automation import Tools
from core import Agent, Cancelled, OpenAIClient
from chatgpt_auth import ChatGPTSession, USAGE_URL
from chatgpt_client import ChatGPTClient
import settings
from voice import LocalTranscriber, Recorder
from runtime import external_program_environment


LANGUAGES = {"Auto-detect": [], "English": ["en"], "বাংলা / Bangla": ["bn"],
             "English + বাংলা": ["en", "bn"], "हिन्दी / Hindi": ["hi"],
             "العربية / Arabic": ["ar"], "Español / Spanish": ["es"],
             "Français / French": ["fr"], "Other language (auto)": []}


class Approval:
    def __init__(self):
        self.event = threading.Event()
        self.allowed = False


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Arafat Assistant · ChatGPT plan or API")
        self.root.geometry("1000x800")
        self.root.minsize(760, 640)
        self.directory = settings.data_directory()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.config_problem = ""
        try:
            self.config = settings.load_config(self.directory)
        except Exception as exc:
            self.config = settings.defaults()
            self.config_problem = str(exc)
        self.api_key, self.remember = settings.read_key()
        self.session = ChatGPTSession(self.directory)
        self.plan_models = []
        self.voice_agreed = False
        self.events, self.jobs = queue.Queue(), queue.Queue()
        self.cancel = threading.Event()
        self.recorder = Recorder()
        self.recording = self.busy = self.closing = False
        self.record_after = None
        self.pending = self.approval_window = None
        self.worker = threading.Thread(target=self._work, daemon=True)
        self.status = tk.StringVar(value="Ready · select Continue with ChatGPT to use your Plus or Pro plan")
        self.connection = tk.StringVar()
        self.plan_model_label = tk.StringVar()
        self.language = tk.StringVar(value="Auto-detect")
        self.windows_access = tk.BooleanVar(value=False)
        self._build()
        self.worker.start()
        self.root.after(80, self._poll)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.log("Assistant", "Welcome, Arafat. Select Continue with ChatGPT to connect your eligible Plus or Pro plan. Allow Use your ChatGPT plan in the browser. This mode uses your existing plan allowance and never switches to paid API access.\n\nVoice: Record → Stop recording → review the locally generated transcript → Run. First use downloads a multilingual speech model; recordings stay on your PC.\n\nBrowser: the assistant uses its own visible Microsoft Edge window. Sign in to websites there manually when needed.\n\nWindows apps: enable the checkbox for this session. Standard accessible controls are supported.\n\nReview proposed actions. Stop takes effect between operations and cannot undo completed work.")
        if self.config_problem:
            self.log("Settings", self.config_problem)
        if self.session.problem:
            self.log("ChatGPT connection", self.session.problem)
        self._update_connection()
        if self.config["auth_mode"] == "chatgpt" and self.session.record:
            self.jobs.put({"kind": "models"})
        elif self.config["auth_mode"] == "api" and self.api_key:
            self.status.set("Ready")

    def _build(self):
        self.root.configure(bg="#eef2f7")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f7")
        style.configure("TLabel", background="#eef2f7", font=("Segoe UI", 10))
        style.configure("TCheckbutton", background="#eef2f7", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 7))
        style.configure("Accent.TButton", background="#1c4f91", foreground="white")
        style.map("Accent.TButton", background=[("active", "#2a64ad")])
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        heading = ttk.Frame(frame)
        heading.pack(fill="x")
        ttk.Label(heading, text="Arafat Assistant", font=("Segoe UI", 22, "bold")).pack(side="left")
        self.settings_button = ttk.Button(heading, text="Settings", command=self.show_settings)
        self.settings_button.pack(side="right")
        ttk.Label(frame, text="Voice or text instructions · English, বাংলা and other supported languages", wraplength=880).pack(anchor="w", pady=(3, 12))
        connection = ttk.Frame(frame)
        connection.pack(fill="x", pady=(0, 8))
        self.connect_button = ttk.Button(connection, text="Continue with ChatGPT", command=self.connect_chatgpt)
        self.connect_button.pack(side="left")
        self.usage_button = ttk.Button(connection, text="Manage usage", command=self.manage_usage)
        self.usage_button.pack(side="left", padx=8)
        ttk.Label(connection, textvariable=self.connection, wraplength=540).pack(side="left", padx=4)
        models = ttk.Frame(frame)
        models.pack(fill="x", pady=(0, 8))
        ttk.Label(models, text="ChatGPT model").pack(side="left", padx=(0, 8))
        self.model_box = ttk.Combobox(models, textvariable=self.plan_model_label, state="disabled", width=60)
        self.model_box.pack(side="left")
        self.model_box.bind("<<ComboboxSelected>>", self._choose_model)
        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(0, 12))
        ttk.Label(controls, text="Speech language").pack(side="left", padx=(0, 8))
        self.language_box = ttk.Combobox(controls, state="readonly", values=list(LANGUAGES), textvariable=self.language, width=23)
        self.language_box.pack(side="left")
        self.windows_check = ttk.Checkbutton(controls, text="Allow Windows app access this session", variable=self.windows_access)
        self.windows_check.pack(side="left", padx=16)
        ttk.Label(frame, text="Activity and replies", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.chat = ScrolledText(frame, height=14, wrap="word", font=("Segoe UI", 11),
                                 bg="white", fg="#15283f", relief="flat", padx=14, pady=12)
        self.chat.pack(fill="both", expand=True, pady=(5, 12))
        self.chat.configure(state="disabled")
        self.chat.tag_config("label", foreground="#1c4f91", font=("Segoe UI", 10, "bold"))
        ttk.Label(frame, text="Your instruction / আপনার নির্দেশ", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.input = ScrolledText(frame, height=4, wrap="word", font=("Segoe UI", 12), relief="flat", padx=10, pady=9)
        self.input.pack(fill="x", pady=6)
        self.input.bind("<Control-Return>", lambda event: self.submit())
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(5, 10))
        self.record_button = ttk.Button(row, text="Record voice", command=self.toggle_record)
        self.record_button.pack(side="left")
        self.run_button = ttk.Button(row, text="Run instruction", style="Accent.TButton", command=self.submit)
        self.run_button.pack(side="left", padx=8)
        self.stop_button = ttk.Button(row, text="Stop task", command=self.stop, state="disabled")
        self.stop_button.pack(side="left")
        self.new_button = ttk.Button(row, text="New conversation", command=self.new_conversation)
        self.new_button.pack(side="right")
        ttk.Button(row, text="Saved notes", command=self.open_output).pack(side="right", padx=8)
        ttk.Label(frame, textvariable=self.status, font=("Segoe UI", 10, "bold"), wraplength=900).pack(anchor="w")
        ttk.Label(frame, text="ChatGPT mode uses your plan allowance. Optional API mode is billed separately. Instructions and selected page/app text go to OpenAI. Speech is transcribed locally. No always-on listening.", foreground="#52657b", wraplength=900, font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 0))

    def _update_connection(self):
        plan = self.config["auth_mode"] == "chatgpt"
        self.connection.set(("Using your ChatGPT plan · " if self.session.plan_enabled() else "ChatGPT plan not enabled · ") + self.session.account_label()
                            if plan else "OpenAI API mode · billed separately")
        usable = not self.busy and not self.closing
        self.connect_button.configure(state="normal" if usable else "disabled")
        self.model_box.configure(state="readonly" if usable and plan and self.plan_models else "disabled")

    def connect_chatgpt(self, client_id=None, new_account=False):
        if self.busy or self.closing:
            return
        self.cancel.clear()
        self._set_busy(True)
        self.status.set("Opening ChatGPT sign-in in your default browser…")
        self.jobs.put({"kind": "connect", "client_id": client_id, "new_account": new_account})

    def manage_usage(self):
        import webbrowser
        with external_program_environment():
            webbrowser.open(USAGE_URL)

    def _choose_model(self, event=None):
        index = self.model_box.current()
        if 0 <= index < len(self.plan_models):
            self.config["plan_model"] = self.plan_models[index]["slug"]
            settings.save_config(self.directory, self.config)
            self.jobs.put({"kind": "clear"})

    def log(self, label, text):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{label}\n", "label")
        self.chat.insert("end", str(text) + "\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _post_log(self, label, text):
        self.events.put(("log", label, text))

    def _approve(self, title, detail):
        approval = Approval()
        self.events.put(("approve", title, detail, approval))
        while not approval.event.wait(0.1):
            if self.cancel.is_set():
                return False
        return approval.allowed and not self.cancel.is_set()

    def _work(self):
        tools = Tools(self.directory / "browser-profile", settings.output_directory(),
                      self.config["apps"], self._approve, self._post_log)
        agent = None
        transcriber = LocalTranscriber(self.directory / "speech-models")
        try:
            while True:
                job = self.jobs.get()
                kind = job["kind"]
                if kind == "shutdown":
                    break
                if kind == "clear":
                    agent = None
                    continue
                try:
                    if kind in ("connect", "models"):
                        if kind == "connect":
                            self.session.sign_in(self.cancel, self._post_log, job.get("client_id"), job.get("new_account", False))
                            self.events.put(("connected",))
                            agent = None
                        self.events.put(("models", self.session.models()))
                        continue
                    if kind == "disconnect":
                        revoked = self.session.disconnect()
                        agent = None
                        self.events.put(("disconnected", revoked))
                        continue
                    if kind == "transcribe":
                        text = transcriber.transcribe(job["audio"], job["languages"], self.cancel, self._post_log)
                        if not self.cancel.is_set():
                            self.events.put(("transcript", text))
                    else:
                        config = job["config"]
                        client = (ChatGPTClient(self.session, config["plan_model"], self.cancel)
                                  if config["auth_mode"] == "chatgpt" else
                                  OpenAIClient(job["key"], config["model"], config["transcription_model"]))
                        tools.cancel = self.cancel
                        tools.desktop_enabled = job["windows"]
                        tools.apps = job["config"]["apps"]
                        if agent is None:
                            agent = Agent(client, tools, self._post_log)
                        agent.client = client
                        text = agent.run(job["text"], self.cancel)
                        self.events.put(("log", "Assistant", text))
                except Cancelled as exc:
                    self.events.put(("log", "Stopped", str(exc)))
                    agent = None  # Discard partial task state after cancellation.
                except Exception as exc:
                    message = str(exc)
                    if job.get("key"):
                        message = message.replace(job["key"], "[key hidden]")
                    self.events.put(("log", "Error", message))
                    agent = None
                finally:
                    job.pop("audio", None)
                    self.events.put(("done",))
        finally:
            tools.close()
            self.events.put(("closed",))

    def _poll(self):
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                if kind == "log":
                    if event[1] == "Status":
                        self.status.set(event[2])
                    else:
                        self.log(event[1], event[2])
                elif kind == "transcript":
                    self.input.configure(state="normal")
                    self.input.delete("1.0", "end")
                    self.input.insert("1.0", event[1])
                    self.log("Voice transcript", event[1] + "\n\nReview or edit this text, then select Run instruction.")
                elif kind == "connected":
                    self.config["auth_mode"] = "chatgpt"
                    settings.save_config(self.directory, self.config)
                    if self.session.plan_enabled():
                        self.log("ChatGPT", "Connected. Using your ChatGPT plan allowance. No API credit is required in this mode.")
                        if not self.config["plan_welcome_seen"]:
                            self.config["plan_welcome_seen"] = True
                            settings.save_config(self.directory, self.config)
                            messagebox.showinfo("You’re using your ChatGPT plan", "Eligible requests use your existing ChatGPT plan allowance. Manage app limits in ChatGPT Settings → Usage.\n\nThis app does not charge a separate fee for ChatGPT mode or switch to paid API access.", parent=self.root)
                    else:
                        self.log("ChatGPT", "Signed in, but plan usage is not enabled. Reconnect and allow Use your ChatGPT plan before running a task.")
                elif kind == "models":
                    self.plan_models = event[1]
                    labels = [f"{model['display_name']} ({model['slug']})" for model in self.plan_models]
                    self.model_box.configure(values=labels)
                    index = next((i for i, model in enumerate(self.plan_models) if model["slug"] == self.config["plan_model"]), 0)
                    self.model_box.current(index)
                    self._choose_model()
                elif kind == "disconnected":
                    self.plan_models = []
                    self.config["plan_model"] = ""
                    self.model_box.set("")
                    self.log("ChatGPT", "Signed out locally. Select Continue with ChatGPT to reconnect. " + ("The renewable session was revoked." if event[1] else "Remote revocation was not confirmed. Disconnect the app in ChatGPT Settings → Security and login → Sign in with ChatGPT."))
                elif kind == "approve":
                    if self.cancel.is_set() or self.closing:
                        event[3].event.set()
                    else:
                        self._show_approval(*event[1:])
                elif kind == "done":
                    self._dismiss_approval(False)
                    self._set_busy(False)
                    self.status.set("Closing after the current operation…" if self.closing else "Ready")
                    self._update_connection()
                elif kind == "closed":
                    self.root.destroy()
                    return
        except queue.Empty:
            pass
        self.root.after(80, self._poll)

    def _show_approval(self, title, detail, approval):
        self.pending = approval
        dialog = tk.Toplevel(self.root)
        self.approval_window = dialog
        dialog.title(title)
        dialog.geometry("760x570")
        dialog.transient(self.root)
        dialog.grab_set()
        box = ttk.Frame(dialog, padding=16)
        box.pack(fill="both", expand=True)
        ttk.Label(box, text=title, font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))
        text = ScrolledText(box, wrap="word", font=("Segoe UI", 11))
        text.pack(fill="both", expand=True)
        text.insert("1.0", detail)
        text.configure(state="disabled")
        buttons = ttk.Frame(box)
        buttons.pack(fill="x", pady=(12, 0))
        ttk.Button(buttons, text="Decline and stop", command=lambda: self._dismiss_approval(False)).pack(side="left")
        ttk.Button(buttons, text="Allow once", style="Accent.TButton", command=lambda: self._dismiss_approval(True)).pack(side="right")
        dialog.protocol("WM_DELETE_WINDOW", lambda: self._dismiss_approval(False))
        dialog.bind("<Escape>", lambda event: self._dismiss_approval(False))
        self.status.set("Waiting for your review")

    def _dismiss_approval(self, allowed):
        if self.pending:
            self.pending.allowed = allowed
            self.pending.event.set()
            self.pending = None
        if self.approval_window:
            self.approval_window.destroy()
            self.approval_window = None

    def _set_busy(self, value):
        self.busy = value
        usable = not value and not self.closing
        for button in (self.run_button, self.record_button, self.settings_button, self.new_button, self.windows_check, self.connect_button):
            button.configure(state="normal" if usable else "disabled")
        self.language_box.configure(state="readonly" if usable else "disabled")
        self.input.configure(state="normal" if usable else "disabled")
        self.stop_button.configure(state="normal" if value and not self.closing else "disabled")
        self._update_connection()

    def _ready(self):
        if self.busy or self.closing:
            return False
        if self.config["auth_mode"] == "chatgpt":
            if not self.session.plan_enabled():
                self.connect_chatgpt()
                return False
            if not self.config["plan_model"]:
                self.cancel.clear()
                self._set_busy(True)
                self.jobs.put({"kind": "models"})
                return False
        elif not self.api_key:
            self.show_settings()
            return False
        return True

    def submit(self):
        if self.recording or not self._ready():
            return "break"
        text = self.input.get("1.0", "end").strip()
        if not text:
            self.status.set("Type an instruction or record your voice first.")
            return "break"
        if len(text) > 20_000:
            messagebox.showinfo("Instruction too long", "Please limit the instruction to 20,000 characters.", parent=self.root)
            return "break"
        self.cancel.clear()
        self.log("You", text)
        self.input.delete("1.0", "end")
        self._set_busy(True)
        self.status.set("Working…")
        self.jobs.put({"kind": "run", "key": self.api_key, "config": copy.deepcopy(self.config),
                       "text": text, "windows": self.windows_access.get()})
        return "break"

    def toggle_record(self):
        if self.recording:
            self._finish_record()
            return
        if not self._ready():
            return
        if not self.voice_agreed:
            agreed = messagebox.askyesno("Local speech recognition",
                "Voice is transcribed on your computer. First use downloads a multilingual speech model from Hugging Face (several hundred MB).\n\nAfter recording, review the transcript before sending it to ChatGPT.\n\nPrepare local speech recognition when you record?", parent=self.root)
            if not agreed:
                return
            self.voice_agreed = True
        if self.input.get("1.0", "end").strip():
            messagebox.showinfo("Keep your draft", "Clear or send the typed instruction before recording a new one.", parent=self.root)
            return
        try:
            self.recorder.start()
        except Exception as exc:
            self.recorder.discard()
            self.log("Microphone", "Could not start recording. Check Windows microphone permissions and the default input device. " + str(exc))
            return
        self.recording = True
        self.record_button.configure(text="Stop recording")
        for item in (self.run_button, self.settings_button, self.new_button, self.windows_check):
            item.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.language_box.configure(state="disabled")
        self.input.configure(state="disabled")
        self.status.set("Recording · select Stop recording when finished · maximum 60 seconds")
        self.record_after = self.root.after(60_000, self._finish_record)

    def _finish_record(self):
        if not self.recording:
            return
        if self.record_after:
            self.root.after_cancel(self.record_after)
            self.record_after = None
        self.recording = False
        self.record_button.configure(text="Record voice")
        try:
            audio = self.recorder.finish()
        except Exception as exc:
            self._set_busy(False)
            self.log("Microphone", str(exc))
            self.status.set("Ready")
            return
        self.cancel.clear()
        self._set_busy(True)
        self.status.set("Transcribing · no task will run until you review the text")
        self.jobs.put({"kind": "transcribe", "key": self.api_key, "config": copy.deepcopy(self.config),
                       "audio": audio, "languages": LANGUAGES[self.language.get()]})

    def stop(self):
        self.cancel.set()
        self._dismiss_approval(False)
        if self.recording:
            if self.record_after:
                self.root.after_cancel(self.record_after)
                self.record_after = None
            self.recording = False
            self.recorder.discard()
            self.record_button.configure(text="Record voice")
            self._set_busy(False)
            self.status.set("Recording discarded")
        else:
            self.status.set("Stopping after the current operation · completed actions cannot be undone")

    def new_conversation(self):
        if self.busy or self.recording:
            return
        self.jobs.put({"kind": "clear"})
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self.log("Assistant", "New conversation. Browser tabs and sign-ins remain open. Tell me what to do.")

    def open_output(self):
        folder = settings.output_directory()
        folder.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(str(folder))
        else:
            messagebox.showinfo("Saved notes", str(folder), parent=self.root)

    def show_settings(self):
        if self.busy or self.recording or self.closing:
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Assistant settings")
        dialog.geometry("740x810")
        dialog.transient(self.root)
        dialog.grab_set()
        box = ttk.Frame(dialog, padding=20)
        box.pack(fill="both", expand=True)
        ttk.Label(box, text="Connection and apps", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        mode = tk.StringVar(value=self.config["auth_mode"])
        ttk.Radiobutton(box, text="Use my ChatGPT Plus / Pro plan · no API key", variable=mode, value="chatgpt").pack(anchor="w", pady=(8, 3))
        ttk.Radiobutton(box, text="Use a separately billed OpenAI API account", variable=mode, value="api").pack(anchor="w")
        ttk.Label(box, text="For Plus / Pro: save these settings, then select Continue with ChatGPT in the main window. Approve Use your ChatGPT plan in your browser. Plan limits apply.", wraplength=680).pack(anchor="w", pady=(8, 6))
        ttk.Label(box, text="Current ChatGPT connection: " + self.session.account_label(), wraplength=680).pack(anchor="w")
        profile_ids = list(self.session.profiles)
        profile_labels = [f"{self.session.profiles[c].get('email') or 'ChatGPT account'} · {c[-10:]}" for c in profile_ids]
        account_choice = ttk.Combobox(box, values=profile_labels + ["Add another ChatGPT account"], state="readonly", width=70)
        account_choice.pack(fill="x", pady=(5, 3))
        account_choice.current(profile_ids.index(self.session.selected_id) if self.session.selected_id in profile_ids else len(profile_ids))

        def connect_selected():
            index = account_choice.current()
            dialog.destroy()
            self.connect_chatgpt(profile_ids[index] if index < len(profile_ids) else None, index == len(profile_ids))

        ttk.Button(box, text="Continue with selected ChatGPT account", command=connect_selected).pack(anchor="w", pady=(0, 4))

        def disconnect():
            dialog.destroy()
            self.cancel.clear()
            self._set_busy(True)
            self.jobs.put({"kind": "disconnect"})

        ttk.Button(box, text="Sign out of active ChatGPT account", command=disconnect).pack(anchor="w", pady=(4, 10))
        ttk.Label(box, text="Optional API key · used only when API mode is selected").pack(anchor="w")
        key = ttk.Entry(box, show="•", width=80)
        key.insert(0, self.api_key)
        key.pack(fill="x", pady=5)
        remember = tk.BooleanVar(value=self.remember)
        ttk.Checkbutton(box, text="Remember key in Windows Credential Manager", variable=remember).pack(anchor="w", pady=(0, 10))
        model = tk.StringVar(value=self.config["model"])
        for label, variable in (("Optional API task model", model),):
            ttk.Label(box, text=label).pack(anchor="w")
            ttk.Entry(box, textvariable=variable).pack(fill="x", pady=(3, 8))
        ttk.Label(box, text="Allowed apps · one alias=absolute .exe path per line").pack(anchor="w", pady=(8, 3))
        apps = ScrolledText(box, height=6, wrap="none", font=("Consolas", 10))
        apps.pack(fill="both", expand=True)
        apps.insert("1.0", "\n".join(f"{name}={path}" for name, path in self.config["apps"].items()))
        ttk.Label(box, text="Speech is processed locally after a first-use model download. ChatGPT credentials are encrypted for your Windows user. App access starts off each time; the browser retains its own sign-ins locally.", wraplength=680, foreground="#52657b").pack(anchor="w", pady=12)

        def save():
            try:
                value = key.get().strip()
                if mode.get() == "api" and not value:
                    raise ValueError("Enter an API key to enable tasks in API mode.")
                aliases = {}
                for line in apps.get("1.0", "end").splitlines():
                    if not line.strip():
                        continue
                    name, sep, path = line.partition("=")
                    name, path = name.strip().lower(), path.strip().strip('"')
                    if not sep or not re.fullmatch(r"[\w-]{1,40}", name):
                        raise ValueError("Use alias=path on each app line, for example notepad=C:\\Windows\\System32\\notepad.exe")
                    if name in aliases:
                        raise ValueError(f"Duplicate app alias: {name}")
                    p = Path(path)
                    if sys.platform == "win32" and (not p.is_absolute() or p.suffix.lower() != ".exe"):
                        raise ValueError("Each app path must be an absolute .exe path without command arguments.")
                    aliases[name] = path
                if not model.get().strip():
                    raise ValueError("The API model field is required.")
                new_config = {"auth_mode": mode.get(), "plan_model": self.config["plan_model"], "plan_welcome_seen": self.config["plan_welcome_seen"],
                              "model": model.get().strip(), "transcription_model": self.config["transcription_model"], "apps": aliases}
                if mode.get() == "api":
                    settings.remember_key(value, remember.get())
                settings.save_config(self.directory, new_config)
                self.config, self.api_key, self.remember = new_config, value, remember.get()
                self.jobs.put({"kind": "clear"})
                self.status.set("Settings saved · Ready")
                self._update_connection()
                if mode.get() == "chatgpt" and self.session.record:
                    self.jobs.put({"kind": "models"})
                dialog.destroy()
            except Exception as exc:
                messagebox.showerror("Check settings", str(exc), parent=dialog)

        row = ttk.Frame(box)
        row.pack(fill="x")
        ttk.Button(row, text="Cancel", command=dialog.destroy).pack(side="left")
        ttk.Button(row, text="Save settings", style="Accent.TButton", command=save).pack(side="right")

    def close(self):
        if self.closing:
            return
        self.closing = True
        self.cancel.set()
        self._dismiss_approval(False)
        if self.recording:
            if self.record_after:
                self.root.after_cancel(self.record_after)
            self.recording = False
            self.recorder.discard()
        self._set_busy(True)
        self.status.set("Closing after the current operation…")
        self.jobs.put({"kind": "shutdown"})


def main():
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
