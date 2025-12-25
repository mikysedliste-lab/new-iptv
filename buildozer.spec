[app]
title = IPTV Master v30
package.name = iptv_v305
package.domain = org.iptv
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 30.5

# Důležité knihovny pro funkční internet a SSL
requirements = python3,kivy==2.2.1,requests,pyjnius,certifi,openssl,urllib3,idna,chardet

orientation = portrait
android.archs = arm64-v8a
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
