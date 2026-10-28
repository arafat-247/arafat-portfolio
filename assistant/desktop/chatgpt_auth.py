"""Official local Sign in with ChatGPT flow. No browser cookies or API keys.

Contract: https://developers.openai.com/siwc/token-sharing-open-source/sign-in
Tokens are encrypted for the current Windows user with DPAPI. The callback
listener binds only to 127.0.0.1 and exists only during an explicit sign-in.
"""
from __future__ import annotations

import base64
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
from pathlib import Path
import re
import secrets
import sys
import threading
import time
from urllib import error, parse, request
import uuid
import webbrowser

from core import Cancelled, check_cancel
from runtime import external_program_environment

ISSUER = "https://auth.openai.com"
AUTHORIZE = ISSUER + "/api/accounts/authorize"
TOKEN = ISSUER + "/api/accounts/oauth/token"
JWKS = ISSUER + "/.well-known/jwks.json"
RESOURCE = "https://api.openai.com/v1"
SCOPES = "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct"
USAGE_URL = "https://chatgpt.com/settings/usage"
PLAN_SCOPE = "chatgpt.tokens.use.direct"


def json_request(url, *, fields=None, token=None):
    headers = {"Accept": "application/json"}
    if fields is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = request.Request(url, data=None if fields is None else parse.urlencode(fields).encode(), headers=headers)
    try:
        with request.urlopen(req, timeout=45) as response:
            data = json.loads(response.read(2_000_000))
        if not isinstance(data, dict):
            raise ValueError("Invalid response")
        return data
    except error.HTTPError as exc:
        # Never echo token responses, callback codes or request bodies.
        if exc.code in (400, 401, 403):
            raise RuntimeError("ChatGPT sign-in or renewal was rejected. Select Continue with ChatGPT again.") from None
        raise RuntimeError(f"ChatGPT connection returned HTTP {exc.code}. Try again later.") from None
    except (error.URLError, TimeoutError, ValueError):
        raise RuntimeError("Could not contact ChatGPT. Check your internet connection and try again.") from None


class ProtectedStore:
    def __init__(self, directory):
        self.path = Path(directory) / "chatgpt-credentials.dat"

    def load(self):
        if not self.path.exists():
            return None
        if sys.platform != "win32":
            raise RuntimeError("ChatGPT credential storage is available in the Windows build.")
        try:
            import win32crypt
            plain = win32crypt.CryptUnprotectData(self.path.read_bytes(), b"ArafatAssistant ChatGPT v1", None, None, 1)[1]
            data = json.loads(plain)
            if not isinstance(data, dict):
                raise ValueError("Invalid credential record")
            return data
        except Exception:
            raise RuntimeError("The saved ChatGPT connection could not be opened. Disconnect it in Settings, then sign in again.") from None

    def save(self, record):
        if sys.platform != "win32":
            raise RuntimeError("ChatGPT credential storage is available in the Windows build.")
        import win32crypt
        plain = json.dumps(record).encode("utf-8")
        encrypted = win32crypt.CryptProtectData(plain, "Arafat Assistant ChatGPT", b"ArafatAssistant ChatGPT v1", None, None, 1)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        temp.write_bytes(encrypted)
        temp.replace(self.path)

    def delete(self):
        self.path.unlink(missing_ok=True)


def verify_identity(encoded, client_id, nonce=None, expected_sub=None):
    import jwt
    try:
        header = jwt.get_unverified_header(encoded)
        # An untrusted token cannot select an arbitrary algorithm or key URL.
        if header.get("alg") != "RS256" or not isinstance(header.get("kid"), str):
            raise ValueError("Unsupported signature")
        keys = json_request(JWKS).get("keys", [])
        matching = [key for key in keys if key.get("kid") == header["kid"] and key.get("kty") == "RSA"]
        if len(matching) != 1:
            raise ValueError("Unknown signing key")
        public = jwt.PyJWK.from_dict(matching[0], algorithm="RS256").key
        claims = jwt.decode(encoded, public, algorithms=["RS256"], audience=client_id,
                            issuer=ISSUER, leeway=30, options={"require": ["sub", "exp", "iat", "iss", "aud"]})
        if not isinstance(claims.get("sub"), str) or not claims["sub"]:
            raise ValueError("Missing identity")
        if nonce is not None and (not isinstance(claims.get("nonce"), str) or
                                  not secrets.compare_digest(claims["nonce"], nonce)):
            raise ValueError("Nonce mismatch")
        if expected_sub is not None and claims["sub"] != expected_sub:
            raise ValueError("Account mismatch")
        return claims
    except Exception:
        raise RuntimeError("ChatGPT identity could not be verified. No connection was saved. Please sign in again.") from None


def callback_values(path, expected_state, existing_client=None):
    parsed = parse.urlsplit(path)
    if parsed.path != "/auth/callback" or len(path) > 16_000:
        raise ValueError("Unexpected callback")
    pairs = parse.parse_qs(parsed.query, keep_blank_values=True)
    if any(len(values) != 1 for values in pairs.values()):
        raise ValueError("Repeated callback parameter")
    values = {name: value[0] for name, value in pairs.items()}
    if not secrets.compare_digest(values.get("state", ""), expected_state):
        raise ValueError("Sign-in state mismatch")
    if values.get("error"):
        raise RuntimeError("ChatGPT sign-in was cancelled or permission was declined. No connection was changed.")
    client_id = values.get("client_id") or existing_client
    if not client_id or not re.fullmatch(r"oaiapp_[A-Za-z0-9_-]{1,180}", client_id):
        raise ValueError("No issued client ID")
    if existing_client and client_id != existing_client:
        raise ValueError("Registered client mismatch")
    if not values.get("code"):
        raise ValueError("No authorisation code")
    return values["code"], client_id


def token_record(data, client_id, claims, previous=None):
    previous = previous or {}
    access = data.get("access_token")
    expiry = data.get("expires_in")
    if not isinstance(access, str) or not access or not isinstance(expiry, (int, float)) or not math.isfinite(expiry) or expiry <= 0:
        raise RuntimeError("ChatGPT returned an incomplete connection. Sign in again.")
    scopes = data.get("scope", " ".join(previous.get("scopes", []))).split()
    if str(data.get("token_type", "Bearer")).lower() != "bearer":
        raise RuntimeError("Unsupported ChatGPT token type.")
    return {"client_id": client_id, "sub": claims["sub"],
            "email": str(claims.get("email", previous.get("email", "")))[:200],
            "access_token": access, "refresh_token": data.get("refresh_token", previous.get("refresh_token", "")),
            "id_token": data.get("id_token", previous.get("id_token", "")),
            "scopes": scopes, "expires_at": time.time() + expiry,
            "earliest_refresh_at": data.get("earliest_refresh_at", 0)}


class ChatGPTSession:
    def __init__(self, directory, store=None):
        self.directory = Path(directory)
        self.store = store or ProtectedStore(directory)
        self.record = None
        self.profiles = {}
        self.selected_id = None
        self.problem = ""
        self.lock = threading.RLock()
        try:
            loaded = self.store.load()
            if loaded and "profiles" in loaded:
                self.profiles = loaded["profiles"]
                self.selected_id = loaded.get("active_id")
            elif loaded and loaded.get("client_id"):
                self.profiles = {loaded["client_id"]: loaded}
                self.selected_id = loaded["client_id"]
            active = self.profiles.get(self.selected_id, {})
            self.record = active if active.get("access_token") else None
        except RuntimeError as exc:
            self.problem = str(exc)

    def account_label(self):
        if not self.record:
            return "Not connected"
        return self.record.get("email") or "ChatGPT account connected"

    def plan_enabled(self):
        return bool(self.record and {PLAN_SCOPE, "resource.invoke"}.issubset(self.record.get("scopes", [])))

    def _persist(self, record):
        profiles = dict(self.profiles)
        profiles[record["client_id"]] = record
        self.store.save({"active_id": record["client_id"], "profiles": profiles})
        self.profiles, self.selected_id = profiles, record["client_id"]
        self.record = record if record.get("access_token") else None

    def _registration(self):
        path = self.directory / "chatgpt-host.json"
        if path.exists():
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                uuid.UUID(str(value["ext_agent_host_id"]).removeprefix("urn:uuid:"))
                return value
            except (ValueError, KeyError, TypeError):
                raise RuntimeError("The local sign-in registration is invalid. Rename chatgpt-host.json and retry.") from None
        value = {"ext_agent_host_id": "urn:uuid:" + str(uuid.uuid4())}
        self.directory.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return value

    def _save_registration(self, value):
        path = self.directory / "chatgpt-host.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(value), encoding="utf-8")
        temporary.replace(path)

    def sign_in(self, cancel, notify=lambda *args: None, client_id=None, new_account=False):
        with self.lock:
            registration = self._registration()
            old = None if new_account else self.profiles.get(client_id or self.selected_id)
            client = old.get("client_id") if old else (None if new_account else registration.get("pending_client_id"))
            state, nonce, verifier = (secrets.token_urlsafe(48) for _ in range(3))
            challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
            result = {}

            class Callback(BaseHTTPRequestHandler):
                def log_message(self, *args):
                    pass  # Callback URLs contain credentials: never log them.

                def do_GET(self):
                    try:
                        code, issued = callback_values(self.path, state, client)
                        result.update(code=code, client_id=issued)
                        status, message = 200, "Authorisation received. Return to Arafat Assistant to finish connecting."
                    except RuntimeError as exc:
                        result["error"] = str(exc)
                        status, message = 400, "Sign-in was declined. You may return to Arafat Assistant."
                    except ValueError:
                        status, message = 400, "This callback could not be verified. Continue in the original sign-in tab."
                    self.send_response(status)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Referrer-Policy", "no-referrer")
                    self.end_headers()
                    self.wfile.write(message.encode())

            with HTTPServer(("127.0.0.1", 0), Callback) as server:
                server.timeout = 0.25
                redirect = f"http://127.0.0.1:{server.server_port}/auth/callback"
                params = {"client_id": client or "dynamic_agent_client", "ext_agent_host_id": registration["ext_agent_host_id"],
                          "response_type": "code", "redirect_uri": redirect, "scope": SCOPES, "resource": RESOURCE,
                          "state": state, "nonce": nonce, "code_challenge_method": "S256", "code_challenge": challenge}
                if not client:
                    params["agent_name_hint"] = "Arafat Assistant"
                if old and old.get("id_token"):
                    params["id_token_hint"] = old["id_token"]
                if old and old.get("email"):
                    params["login_hint"] = old["email"]
                with external_program_environment():
                    opened = webbrowser.open(AUTHORIZE + "?" + parse.urlencode(params))
                if not opened:
                    raise RuntimeError("Could not open your default browser. Set a Windows default browser and retry.")
                notify("Status", "Sign in in your browser and allow Use your ChatGPT plan. Select Stop task to cancel.")
                deadline = time.monotonic() + 300
                while not result:
                    check_cancel(cancel)
                    if time.monotonic() > deadline:
                        raise RuntimeError("ChatGPT sign-in timed out. Select Continue with ChatGPT to try again.")
                    server.handle_request()
            if "error" in result:
                raise RuntimeError(result["error"])
            check_cancel(cancel)
            registration["pending_client_id"] = result["client_id"]
            self._save_registration(registration)
            data = json_request(TOKEN, fields={"grant_type": "authorization_code", "client_id": result["client_id"],
                                "code": result["code"], "code_verifier": verifier, "redirect_uri": redirect, "resource": RESOURCE})
            claims = verify_identity(data.get("id_token", ""), result["client_id"], nonce,
                                     old.get("sub") if old else None)
            record = token_record(data, result["client_id"], claims)
            check_cancel(cancel)
            self._persist(record)
            registration.pop("pending_client_id", None)
            self._save_registration(registration)
            self.problem = ""

    def access_token(self):
        with self.lock:
            record = self.record
            if not self.plan_enabled():
                raise RuntimeError("Select Continue with ChatGPT and allow Use your ChatGPT plan first.")
            now = time.time()
            if record.get("expires_at", 0) > now + 60:
                return record["access_token"]
            earliest = record.get("earliest_refresh_at", 0)
            if isinstance(earliest, (int, float)) and now < earliest:
                if record.get("expires_at", 0) > now:
                    return record["access_token"]
                raise RuntimeError("ChatGPT token renewal is not available yet. Try again later.")
            if not record.get("refresh_token"):
                raise RuntimeError("Your ChatGPT connection expired. Select Continue with ChatGPT again.")
            data = json_request(TOKEN, fields={"grant_type": "refresh_token", "client_id": record["client_id"],
                                "refresh_token": record["refresh_token"], "resource": RESOURCE})
            claims = {"sub": record["sub"], "email": record.get("email", "")}
            if data.get("id_token"):
                claims = verify_identity(data["id_token"], record["client_id"], expected_sub=record["sub"])
            renewed = token_record(data, record["client_id"], claims, record)
            # Persist a rotated refresh token before any following API request.
            self._persist(renewed)
            return renewed["access_token"]

    def models(self):
        data = json_request(RESOURCE + "/models", token=self.access_token())
        models = [{"slug": item["slug"], "display_name": item.get("display_name") or item["slug"]}
                  for item in data.get("models", []) if isinstance(item, dict) and item.get("visibility") == "list"
                  and isinstance(item.get("slug"), str) and item["slug"]]
        if not models:
            raise RuntimeError("No ChatGPT models were available for this connection. Check your plan and account, then reconnect.")
        return models

    def _revoke(self, record):
        if not record.get("refresh_token"):
            return True
        try:
            endpoint = json_request(ISSUER + "/.well-known/openid-configuration").get("revocation_endpoint")
            parsed = parse.urlsplit(endpoint or "")
            if parsed.scheme != "https" or parsed.netloc != "auth.openai.com":
                return False
            body = parse.urlencode({"token": record["refresh_token"], "token_type_hint": "refresh_token",
                                    "client_id": record["client_id"]}).encode()
            for attempt in range(2):
                try:
                    req = request.Request(endpoint, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                    with request.urlopen(req, timeout=10) as response:
                        return response.status == 200
                except (error.URLError, TimeoutError):
                    if attempt == 0:
                        time.sleep(0.5)
            return False
        except Exception:
            return False

    def disconnect(self):
        with self.lock:
            old = self.record
            revoked = self._revoke(old) if old else True
            if old:
                metadata = {key: old.get(key, "") for key in ("client_id", "sub", "email")}
                self._persist(metadata)
            self.record, self.problem = None, ""
            return revoked
