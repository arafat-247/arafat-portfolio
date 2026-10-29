#!/usr/bin/env bash
set -euo pipefail
mkdir -p device-reports
collect() {
  result=$?
  trap - EXIT
  adb logcat -d > device-reports/logcat.txt 2>&1 || true
  adb shell dumpsys package com.arafat.assistant.voice > device-reports/package.txt 2>&1 || true
  adb pull /sdcard/Download/arafat-voice-main.png device-reports/main.png || true
  exit "$result"
}
trap collect EXIT
adb install --no-incremental apk/ArafatVoice-Android.apk
adb install -t apk/voice-debug-androidTest.apk
adb shell am instrument -w com.arafat.assistant.voice.test/androidx.test.runner.AndroidJUnitRunner | tee device-reports/instrumentation.txt
python3 - <<'PY'
from pathlib import Path
import re
s=Path('device-reports/instrumentation.txt').read_text()
assert re.search(r'OK \([1-9][0-9]* tests?\)',s), s
assert 'FAILURES' not in s and 'INSTRUMENTATION_FAILED' not in s, s
PY
