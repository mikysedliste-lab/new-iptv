
[app]
title = IPTV App
package.name = iptvapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1
# Zůstáváme u stabilní verze 2.2.1
requirements = python3,kivy==2.2.1,requests,pyjnius,certifi,openssl

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True
p4a.branch = develop

[buildozer]
log_level = 2
