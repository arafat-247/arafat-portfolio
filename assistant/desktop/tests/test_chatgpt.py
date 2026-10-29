import copy
import io
import json
import queue
from pathlib import Path
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from urllib import parse, request

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chatgpt_auth as auth
from chatgpt_client import ChatGPTClient, read_stream
from core import Cancelled, TOOL_SCHEMAS
import settings
from voice import LocalTranscriber


class MemoryStore:
    def __init__(self, value=None):
        self.value = value

    def load(self):
        return copy.deepcopy(self.value)

    def save(self, value):
        self.value = copy.deepcopy(value)

    def delete(self):
        self.value = None


def credentials(**values):
    result = {"client_id": "oaiapp_test", "sub": "account-1", "email": "person@example.com",
              "access_token": "test-access", "refresh_token": "test-refresh", "id_token": "test-id",
              "scopes": auth.SCOPES.split(), "expires_at": time.time() + 3600}
    result.update(values)
    return result


def stream(*events):
    return io.BytesIO(b"".join(b"data: " + json.dumps(event, ensure_ascii=False).encode() + b"\n\n" for event in events))


class ChatGPTTests(unittest.TestCase):
    def test_callback_rejects_missing_wrong_repeated_state_and_wrong_client(self):
        for path in ("/auth/callback?code=secret&client_id=oaiapp_test", "/auth/callback?state=bad&code=secret&client_id=oaiapp_test",
                     "/auth/callback?state=good&state=good&code=secret&client_id=oaiapp_test",
                     "/callback?state=good&code=secret&client_id=oaiapp_test",
                     "/auth/callback?state=good&code=secret&client_id=dynamic_agent_client"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                auth.callback_values(path, "good")
        with self.assertRaises(ValueError):
            auth.callback_values("/auth/callback?state=good&code=secret&client_id=oaiapp_changed", "good", "oaiapp_original")
        self.assertEqual(auth.callback_values("/auth/callback?state=good&code=secret", "good", "oaiapp_original"),
                         ("secret", "oaiapp_original"))

    def test_declined_callback_stops_before_code_exchange(self):
        with self.assertRaisesRegex(RuntimeError, "declined"):
            auth.callback_values("/auth/callback?state=good&error=access_denied", "good")

    def test_real_signature_issuer_audience_nonce_and_account_are_verified(self):
        import jwt
        from cryptography.hazmat.primitives.asymmetric import rsa
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
        jwk["kid"] = "test-key"
        claims = {"sub": "account-1", "iss": auth.ISSUER, "aud": "oaiapp_test", "nonce": "nonce",
                  "iat": int(time.time()), "exp": int(time.time()) + 120}
        def encoded(**changes):
            return jwt.encode(dict(claims, **changes), key, algorithm="RS256", headers={"kid": "test-key"})
        with patch("chatgpt_auth.json_request", return_value={"keys": [jwk]}):
            self.assertEqual(auth.verify_identity(encoded(), "oaiapp_test", "nonce", "account-1")["sub"], "account-1")
            for change in ({"iss": "https://wrong.example"}, {"aud": "oaiapp_wrong"}, {"nonce": "wrong"},
                           {"sub": "different-account"}, {"exp": int(time.time()) - 120}):
                with self.subTest(change=change), self.assertRaises(RuntimeError):
                    auth.verify_identity(encoded(**change), "oaiapp_test", "nonce", "account-1")
            unsigned = jwt.encode(claims, "", algorithm="none")
            with self.assertRaises(RuntimeError):
                auth.verify_identity(unsigned, "oaiapp_test", "nonce")

    def test_plan_permission_is_required_even_with_verified_identity(self):
        record = auth.token_record({"access_token": "x", "expires_in": 3600, "scope": "openid email"}, "oaiapp_test", {"sub": "account-1"})
        with tempfile.TemporaryDirectory() as folder:
            session = auth.ChatGPTSession(folder, MemoryStore(record))
            self.assertFalse(session.plan_enabled())
            with self.assertRaisesRegex(RuntimeError, "allow Use your ChatGPT plan"):
                session.access_token()

    def test_sign_in_binds_real_loopback_callback_and_exact_pkce_exchange(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MemoryStore()
            session = auth.ChatGPTSession(folder, store)
            seen = {}
            callback_threads = []
            def open_browser(url):
                params = {k: v[0] for k, v in parse.parse_qs(parse.urlsplit(url).query).items()}
                seen.update(params)
                self.assertEqual(params["client_id"], "dynamic_agent_client")
                self.assertEqual(params["agent_name_hint"], "Arafat Assistant")
                self.assertEqual(parse.urlsplit(params["redirect_uri"]).hostname, "127.0.0.1")
                def callback():
                    address = params["redirect_uri"] + "?" + parse.urlencode({"state": params["state"], "code": "test-code", "client_id": "oaiapp_test"})
                    with request.urlopen(address, timeout=5) as response:
                        self.assertNotIn("test-code", response.read().decode())
                thread = threading.Thread(target=callback)
                thread.start()
                callback_threads.append(thread)
                return True
            data = {"access_token": "test-access", "refresh_token": "test-refresh", "id_token": "test-id",
                    "expires_in": 3600, "scope": auth.SCOPES}
            with patch("chatgpt_auth.webbrowser.open", side_effect=open_browser), \
                 patch("chatgpt_auth.json_request", return_value=data) as post, \
                 patch("chatgpt_auth.verify_identity", return_value={"sub": "account-1", "email": "person@example.com"}) as verify:
                session.sign_in(threading.Event())
            for thread in callback_threads:
                thread.join(timeout=5)
                self.assertFalse(thread.is_alive())
            fields = post.call_args.kwargs["fields"]
            self.assertEqual(fields["redirect_uri"], seen["redirect_uri"])
            self.assertEqual(fields["client_id"], "oaiapp_test")
            challenge = auth.base64.urlsafe_b64encode(auth.hashlib.sha256(fields["code_verifier"].encode()).digest()).rstrip(b"=").decode()
            self.assertEqual(challenge, seen["code_challenge"])
            self.assertEqual(verify.call_args.args[2], seen["nonce"])
            self.assertEqual(store.value["profiles"]["oaiapp_test"]["sub"], "account-1")
            host = json.loads((Path(folder) / "chatgpt-host.json").read_text())
            self.assertNotIn("pending_client_id", host)
            self.assertNotIn("test-access", json.dumps(host))

    def test_refresh_rotates_and_persists_credentials_before_use(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MemoryStore(credentials(expires_at=0))
            session = auth.ChatGPTSession(folder, store)
            data = {"access_token": "new-access", "refresh_token": "new-refresh", "expires_in": 3600, "scope": auth.SCOPES}
            with patch("chatgpt_auth.json_request", return_value=data) as post:
                self.assertEqual(session.access_token(), "new-access")
            self.assertEqual(store.value["profiles"]["oaiapp_test"]["refresh_token"], "new-refresh")
            self.assertEqual(post.call_args.kwargs["fields"]["refresh_token"], "test-refresh")
            self.assertEqual(session.access_token(), "new-access")
            self.assertEqual(post.call_count, 1)

    def test_refresh_identity_mismatch_never_replaces_active_record(self):
        with tempfile.TemporaryDirectory() as folder:
            original = credentials(expires_at=0)
            store = MemoryStore(original)
            session = auth.ChatGPTSession(folder, store)
            with patch("chatgpt_auth.json_request", return_value={"id_token": "wrong"}), \
                 patch("chatgpt_auth.verify_identity", side_effect=RuntimeError("mismatch")):
                with self.assertRaises(RuntimeError):
                    session.access_token()
            self.assertEqual(store.value, original)

    def test_discovery_only_shows_available_visible_models_in_server_order(self):
        with tempfile.TemporaryDirectory() as folder:
            session = auth.ChatGPTSession(folder, MemoryStore(credentials()))
            models = [{"slug": "hidden", "visibility": "hidden"}, {"slug": "second", "display_name": "Second", "visibility": "list"},
                      {"slug": "first", "visibility": "list"}]
            with patch("chatgpt_auth.json_request", return_value={"models": models}):
                self.assertEqual([m["slug"] for m in session.models()], ["second", "first"])

    def test_sse_requires_completion_and_preserves_unicode(self):
        final = {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "বাংলা"}]}]}
        self.assertEqual(read_stream(stream({"type": "response.completed", "response": final}), threading.Event()), final)
        with self.assertRaisesRegex(RuntimeError, "before completion"):
            read_stream(stream({"type": "response.output_text.delta", "delta": "partial"}), threading.Event())
        with self.assertRaisesRegex(RuntimeError, "allowance"):
            read_stream(stream({"type": "response.failed", "response": {"error": {"code": "subscription_sharing_usage_limit_exceeded"}}}), threading.Event())
        cancelled = threading.Event()
        cancelled.set()
        with self.assertRaises(Cancelled):
            read_stream(stream({"type": "response.completed", "response": final}), cancelled)

    def test_plan_requests_use_public_endpoint_namespaces_and_no_paid_fields(self):
        session = Mock()
        session.access_token.return_value = "test-token"
        final = {"type": "response.completed", "response": {"status": "completed", "output": []}}
        response = stream(final)
        response.__enter__ = lambda obj: obj
        with patch("chatgpt_client.request.urlopen", return_value=response) as opened:
            ChatGPTClient(session, "model-from-discovery").response([{"role": "user", "content": "বাংলা"}], TOOL_SCHEMAS)
        req = opened.call_args.args[0]
        payload = json.loads(req.data)
        self.assertEqual(req.full_url, "https://api.openai.com/v1/responses")
        self.assertTrue(payload["stream"])
        self.assertFalse(payload["store"])
        self.assertNotIn("max_output_tokens", payload)
        self.assertEqual(payload["tools"][0]["type"], "namespace")
        self.assertEqual(payload["tools"][0]["tools"], TOOL_SCHEMAS)

    def test_local_voice_handles_bangla_and_mixed_language_without_api(self):
        transcriber = LocalTranscriber(Path("unused"))
        transcriber.model = Mock()
        transcriber.model.transcribe.return_value = (iter([SimpleNamespace(text="নোটপ্যাড "), SimpleNamespace(text="খোলো")]), None)
        self.assertEqual(transcriber.transcribe(b"wave", ["bn"], threading.Event()), "নোটপ্যাড খোলো")
        self.assertEqual(transcriber.model.transcribe.call_args.kwargs["language"], "bn")
        transcriber.model.transcribe.return_value = (iter([SimpleNamespace(text="Open নোটপ্যাড")]), None)
        transcriber.transcribe(b"wave", ["en", "bn"], threading.Event())
        self.assertIsNone(transcriber.model.transcribe.call_args.kwargs["language"])

    def test_existing_api_settings_migrate_to_plan_mode_without_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            (directory / "settings.json").write_text(json.dumps({"model": "old-model", "apps": {}}))
            config = settings.load_config(directory)
            self.assertEqual(config["auth_mode"], "chatgpt")
            config["access_token"] = "must-not-persist"
            settings.save_config(directory, config)
            self.assertNotIn("must-not-persist", (directory / "settings.json").read_text())

    def test_sign_out_attempts_revocation_clears_only_selected_tokens_and_keeps_mapping(self):
        with tempfile.TemporaryDirectory() as folder:
            other = credentials(client_id="oaiapp_other", sub="account-2")
            store = MemoryStore({"active_id": "oaiapp_test", "profiles": {"oaiapp_test": credentials(), "oaiapp_other": other}})
            session = auth.ChatGPTSession(folder, store)
            with patch.object(session, "_revoke", return_value=False) as revoke:
                self.assertFalse(session.disconnect())
            revoke.assert_called_once()
            self.assertIsNone(session.record)
            signed_out = store.value["profiles"]["oaiapp_test"]
            self.assertEqual(signed_out["sub"], "account-1")
            self.assertNotIn("access_token", signed_out)
            self.assertNotIn("refresh_token", signed_out)
            self.assertEqual(store.value["profiles"]["oaiapp_other"], other)

    def test_plan_failure_never_falls_back_to_paid_api_and_error_stays_readable(self):
        from app import Application
        with tempfile.TemporaryDirectory() as folder:
            app = Application.__new__(Application)
            app.directory = Path(folder)
            app.config = settings.defaults()
            app.config["auth_mode"] = "chatgpt"
            app.config["plan_model"] = "discovered-model"
            app.session = Mock()
            app.jobs, app.events = queue.Queue(), queue.Queue()
            app.cancel = threading.Event()
            app.jobs.put({"kind": "run", "key": "", "config": app.config, "text": "Hello", "windows": False})
            app.jobs.put({"kind": "shutdown"})
            with patch("app.ChatGPTClient") as plan, patch("app.OpenAIClient") as paid:
                plan.return_value.response.side_effect = RuntimeError("Plan allowance reached")
                app._work()
                paid.assert_not_called()
            self.assertIn(("log", "Error", "Plan allowance reached"), list(app.events.queue))


if __name__ == "__main__":
    unittest.main()
