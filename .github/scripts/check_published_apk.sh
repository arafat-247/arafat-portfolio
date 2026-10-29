#!/usr/bin/env bash
set -euo pipefail
api="$1"
mkdir -p install-check
finish() {
  result=$?
  trap - EXIT
  adb logcat -d -b all > "install-check/logcat-api-${api}.txt" 2>&1 || true
  adb shell df -h /data > "install-check/storage-api-${api}.txt" 2>&1 || true
  exit "$result"
}
trap finish EXIT
# The boot-completed property can precede package-service readiness on a cold image.
ready=false
for attempt in $(seq 1 20); do
  if adb shell cmd package list packages android > "install-check/package-service-api-${api}.txt" 2>&1; then ready=true; break; fi
  sleep 2
done
if [ "$ready" != true ]; then echo 'Android package service did not become ready'; exit 1; fi
sleep 5
adb install --no-incremental install-check/ArafatAssistant-Android.apk
adb shell am start -W -n com.arafat.assistant/.MainActivity
adb shell pidof com.arafat.assistant
adb shell screencap -p /sdcard/Download/install-check.png
adb pull /sdcard/Download/install-check.png "install-check/install-api-${api}.png"
adb shell dumpsys package com.arafat.assistant > "install-check/package-api-${api}.txt"
