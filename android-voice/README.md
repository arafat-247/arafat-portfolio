# Arafat Voice for Android

A separate, limited voice-dictation and text companion requested after Play Protect blocked the full-control assistant on a Pixel 7. The application ID is `com.arafat.assistant.voice` and the launcher name is **Arafat Voice**. Download **ArafatVoice-Android.apk** from an `assistant-voice-v0.1.*` release, not the older full-control APK.

Follow [QUICK_START.txt](QUICK_START.txt). It accepts typed text or a reviewed transcript from Android's installed speech recognition activity, then returns text using an eligible account's existing ChatGPT plan. English, Bangla Bangladesh/India and the phone language can be requested; the speech provider determines actual support. There is no always-on listening or spoken-response feature.

## No device-control capability

This is a separate Gradle project. It shares only `AuthSession`, `Http`, `Protocol` and `SecureStore` from the original app. It does not compile the original activity, agent, control client or accessibility service. The merged APK must contain exactly the INTERNET permission, one launcher activity and no services, receivers or providers. CI checks both the compiled manifest and DEX, then checks the installed package on Android 15 and 17 emulators. No accessibility, SMS, notification, microphone, overlay or storage permission is requested.

The AI receives no tools and has no action executor. Unexpected tool output rejects the entire reply. It cannot inspect screens, control apps, browse links, read files or import ChatGPT history. Users can paste text manually. Only completed replies enter in-memory history; at most eight complete exchanges are kept. New conversation, a model change or process loss clears context. An overlong conversation asks the user to start fresh. Stop cancels the pending request.

## Connection and limits

The shared client uses the official [open-source Sign in with ChatGPT flow](https://developers.openai.com/siwc/token-sharing-open-source). Account and workspace eligibility remain controlled by OpenAI. Requests use the selected account's current model catalog, the public Responses endpoint, `store:false` and `stream:true`; no API-key mode or paid API fallback is implemented. This does not guarantee that any particular ChatGPT account can connect. Tokens are encrypted with Android Keystore, excluded from backup and never printed by the app. No live user sign-in or inference request runs in CI.

## Installation restrictions remain possible

Removing accessibility capability addresses the sensitive-permission trigger described in [Google's Play Protect developer guidance](https://developers.google.com/android/play-protect/warning-dev-guidance). It does not certify this app as safe, approved or installable on every device. [Android Advanced Protection](https://support.google.com/android/answer/16339980) can block apps from unknown sources even without those permissions. Keep Play Protect and Advanced Protection enabled. If installation is blocked, report the exact warning; this guide does not ask users to disable protection or bypass a warning.

This is a debug-signed personal preview, not a Google Play release. CI's temporary debug identity may change, so later previews may require reinstalling this app and reconnecting. Do not uninstall ChatGPT or the other assistant to install this separately named package.

## Build and checks

JDK 17, Gradle 8.13, Android SDK 35 and AGP 8.11.1:

```sh
gradle -p android-voice testDebugUnitTest lintDebug assembleDebug assembleDebugAndroidTest
python3 android-voice/check_apk.py android-voice/app/build/outputs/apk/debug/app-debug.apk "$ANDROID_HOME/cmdline-tools/latest/bin/apkanalyzer"
```

`.github/workflows/assistant-voice.yml` builds once, checks the delivered APK, installs normally without `-t`, and runs the separate test APK on Android 15 and 17. Only the instrumentation APK uses `-t`. Device checks verify the installed permissions/components, visible onboarding, encrypted storage and a simulated Bangla dictation transcript that requires Send. Unit checks cover text-only requests, unsupported tool rejection, incomplete streams, cancellation and bounded transactional history. These do not test real microphone recognition, live ChatGPT login or Google Play Protect's physical-device verdict.

Source licence: [MIT](../assistant/LICENSE).
