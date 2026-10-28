# Arafat Assistant for Android

A personal, open-source Android companion for typed or dictated instructions and approved actions in selected apps. The Windows app remains separate. This module creates a sideloadable testing APK through `.github/workflows/assistant-android.yml`.

## Install and first task

Follow [QUICK_START.txt](QUICK_START.txt). The tested APK and SHA-256 checksum are published only after the build, unit tests, lint and Android 15 emulator checks pass. Download from the repository's **assistant-android-v0.1.*** releases; a Windows ZIP cannot run on Android.

1. Install `ArafatAssistant-Android.apk` on Android 8 or later. If requested, allow the browser/file app to install this package. Keep Play Protect enabled.
2. Open **Continue with ChatGPT**, sign in in your system browser, and allow **Use your ChatGPT plan** where available. Return to the assistant when the browser says the callback was received.
3. Choose an account-available model. Type `বাংলায় উত্তর দাও।` and press **Run instruction**.
4. For dictation select English, Bangla (Bangladesh/India), or Phone language. The phone language setting lets you request another language supported by your installed speech provider. Review the transcript before Run. Keyboard dictation is another option.
5. For app control, read the disclosure, enable the service in Android Accessibility settings, select apps, and tick the sharing checkbox for this task. Websites use a selected browser app. The assistant moves into a visible floating approval panel. **Approve** allows one proposed change, **Move** repositions the panel, **Stop** ends access, and **Return** stops and reopens the assistant.

Only enable the accessibility service if you want the disclosed functionality. Android may restrict sideloaded services; the app cannot enable itself or bypass system restrictions. Installation details vary by phone. Android's [restricted-settings guidance](https://support.google.com/android/answer/12623953) explains those controls. This is a personal sideloaded preview, not a Play Store submission or a claim of Play Store policy compliance.

## ChatGPT connection and cost

Uses the official local/open-source [Sign in with ChatGPT](https://developers.openai.com/siwc/quickstart) flow. Eligible accounts can authorise plan-backed Responses requests; availability, account/workspace eligibility and shared limits are controlled by OpenAI. **There is no API-key field, automatic API fallback or separate API billing configured in this app.** An existing subscription does not guarantee eligibility for this preview.

The native Android implementation binds an ephemeral loopback listener to `127.0.0.1`, opens the system browser, validates callback state and PKCE, validates the RS256 ID token against OpenAI JWKS, checks issuer/audience/expiry/nonce/identity, and checks both plan scopes. It uses a stable per-installation host ID and reuses the issued registration ID. Tokens are encrypted with AES-GCM using Android Keystore, excluded from backup and never logged. Renewal is serialised, persists rotation before inference and preserves the verified identity. Sign out attempts discovery-based token revocation and removes local tokens. This first preview keeps one active account registration; disconnect in ChatGPT settings if you need to revoke an old one. Reset local connection removes unreadable local credentials while retaining registration metadata.

Models come from the selected account's live `/v1/models` list. Requests use `https://api.openai.com/v1/responses`, `store:false`, `stream:true`, namespaced function tools and full in-memory task context. Only a completed SSE response can lead to tool execution. Interrupted, failed or incomplete streams do not authorise actions. There is no use of ChatGPT cookies, unofficial backend endpoints or credentials from another app. ChatGPT conversations/memories are not imported.

OpenAI's [plan route limitations](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations) exclude transcription. Voice therefore opens Android's installed speech recognition activity. Its provider handles audio and may use online services; the offline preference is a hint. No microphone recording is captured by this companion, and it has no microphone permission. The recognised text goes to OpenAI only when you press Run.

## Scope of app access

The accessibility service ignores event contents and reads only on demand during a task. Both selected packages and task-specific consent are required. It reads at most 80 visible accessible nodes, skips password/sensitive subtrees, and offers `read_screen`, `click`, `type_text`, `scroll`, `open_url`, `launch_app` and `back`. Every state-changing tool requires a visible user approval. A control's package, path, fingerprint and freshness are rechecked after approval. References are invalidated after changes. Own screens, Android settings, System UI and permission controllers are excluded. Selected apps may still display sensitive content that is not marked by Android; do not select confidential apps.

There is no raw coordinate click, screenshot capture, arbitrary shell, root access, ADB requirement, hidden screen monitoring, notification collection, wake-word listener, or automatic permission grant. Android's standard accessible controls do not work in every app. Handle authentication, payments, permissions and other sensitive flows yourself. Each Run starts a new task with at most 16 model turns; activity replies are kept only in process memory, capped at 40 entries.

## Build and verification

JDK 17, Gradle 8.13, Android SDK 35/Build Tools 35, AGP 8.11.1. Open the `android` directory in Android Studio, or install the specified Gradle and run:

```sh
gradle testDebugUnitTest lintDebug assembleDebug assembleDebugAndroidTest
# With a running Android 15 emulator:
gradle connectedDebugAndroidTest
```

Tests cover PKCE, duplicate/state/client callback rejection, real RSA signature validation and identity checks, plan scopes, partial stream rejection, cancellation, supported request fields, tool namespaces and Unicode tool results. Emulator tests open the packaged UI, round-trip Keystore encryption, read a separate fixture app, exclude a password node, require a real Approve tap before a click, invalidate stale nodes, reject an unselected foreground app, and enforce Stop. The fixture exists only in the test APK and is not included in the download.

Live ChatGPT sign-in/inference, real microphone dictation and arbitrary installed-app workflows are **not** tested by CI. They require a local trial. No account token or live paid request is used by the tests. All network origins in the AI/auth client are fixed official HTTPS origins.

The published APK is **debug-signed for personal testing**, with an ephemeral CI test key, not a production signing identity. A later build may require uninstall/reinstall, which erases local connection data. For updates with a stable identity, build and sign with your own private release key. Never commit a private signing key or credentials. Keep the OS and Play Protect enabled.

## Licence and sources

Assistant source: [MIT](../assistant/LICENSE). Android framework is used through its public APIs. See [Android accessibility service documentation](https://developer.android.com/guide/topics/ui/accessibility/service), [speech recognition intent](https://developer.android.com/reference/android/speech/RecognizerIntent), and the linked official OpenAI documentation.
