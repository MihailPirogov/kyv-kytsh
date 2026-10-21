#!/bin/bash
# Signed release APK + AAB of Кыв кытш -> release/kyv-kytsh.apk, release/kyv-kytsh.aab
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build_release.py android
export JAVA_HOME="${JAVA_HOME:-$HOME/jdk17}"; export PATH="$JAVA_HOME/bin:$PATH"
export ANDROID_HOME="${ANDROID_HOME:-$HOME/android-sdk}"
GRADLE="${GRADLE:-gradle}"; command -v "$GRADLE" >/dev/null || GRADLE=$(ls -d $HOME/.gradle/wrapper/dists/gradle-8.13-bin/*/gradle-8.13)/bin/gradle
(cd android && "$GRADLE" --no-daemon -q assembleRelease) && (cd android && "$GRADLE" --no-daemon -q bundleRelease)
cp android/app/build/outputs/apk/release/app-release.apk release/kyv-kytsh.apk
cp android/app/build/outputs/bundle/release/app-release.aab release/kyv-kytsh.aab
BT="$ANDROID_HOME/build-tools/36.0.0"
$BT/apksigner verify release/kyv-kytsh.apk && echo "apk signature OK"
$BT/aapt2 dump badging release/kyv-kytsh.apk | grep -E "^package|minSdk|targetSdk|application-label:"
$BT/aapt2 dump permissions release/kyv-kytsh.apk | grep -o "name='[^']*'" | tr '\n' ' '; echo
# ad units: real IDs unless built with -PadsDemo=true (see android/app/src/main/res/values/ads.xml)
if grep -q 'R-M-[0-9]' android/app/src/main/res/values/ads.xml; then grep -o 'R-M-[0-9]*-[0-9]*' android/app/src/main/res/values/ads.xml | tr '\n' ' '; echo "(real Yandex Mobile Ads units)"; else echo "WARNING: ads.xml still has PLACEHOLDER demo units (demo-*-yandex): test ads only, no revenue"; fi
ls -la release/kyv-kytsh.apk release/kyv-kytsh.aab
