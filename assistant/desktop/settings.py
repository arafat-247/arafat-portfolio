"""User preferences and optional Windows Credential Manager storage."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys

from core import DEFAULT_MODEL, DEFAULT_TRANSCRIBE_MODEL


def data_directory():
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ArafatAssistant"
    return Path.home() / ".local" / "share" / "ArafatAssistant"


def output_directory():
    documents = Path.home() / "Documents"
    if sys.platform == "win32":
        try:
            import ctypes
            buffer = ctypes.create_unicode_buffer(32768)
            if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buffer) == 0:
                documents = Path(buffer.value)
        except Exception:
            pass
    return documents / "ArafatAssistant"


def defaults():
    root = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32"
    return {"model": DEFAULT_MODEL, "transcription_model": DEFAULT_TRANSCRIBE_MODEL,
            "apps": {"notepad": str(root / "notepad.exe"),
                     "calculator": str(root / "calc.exe"),
                     "paint": str(root / "mspaint.exe")}}


def load_config(directory):
    base = defaults()
    path = directory / "settings.json"
    if not path.exists():
        return base
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("apps", {}), dict):
        raise ValueError("Invalid settings.json. Rename it and start again, or correct its app list.")
    for key in ("model", "transcription_model"):
        if isinstance(value.get(key), str) and value[key].strip():
            base[key] = value[key].strip()
    if "apps" in value:
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in value["apps"].items()):
            raise ValueError("App aliases and executable paths must be text.")
        base["apps"] = value["apps"]
    return base


def save_config(directory, config):
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "settings.json"
    temporary = directory / "settings.tmp"
    # Never persist the API key in this JSON file.
    clean = {key: config[key] for key in ("model", "transcription_model", "apps")}
    temporary.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(target)


def vault():
    if sys.platform != "win32":
        raise ValueError("Remembering an API key is supported only on Windows.")
    from keyring.backends.Windows import WinVaultKeyring
    return WinVaultKeyring()


def read_key():
    value = os.environ.get("OPENAI_API_KEY", "").strip()
    if value:
        return value, False
    try:
        value = vault().get_password("ArafatAssistant", "openai-api-key") or ""
        return value, bool(value)
    except Exception:
        return "", False


def remember_key(value, remember):
    if remember:
        vault().set_password("ArafatAssistant", "openai-api-key", value)
    else:
        try:
            store = vault()
            if store.get_password("ArafatAssistant", "openai-api-key"):
                store.delete_password("ArafatAssistant", "openai-api-key")
        except Exception as exc:
            if sys.platform == "win32":
                raise RuntimeError("Could not remove the saved key from Windows Credential Manager.") from exc
