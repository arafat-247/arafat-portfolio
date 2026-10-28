#!/usr/bin/env bash
# Keep the real Gradle result, including when collecting diagnostic images fails.
set +e
gradle --no-daemon connectedDebugAndroidTest
check_status=$?
adb pull /sdcard/Android/data/com.arafat.assistant/files app/build/reports/device-screens
exit "$check_status"
