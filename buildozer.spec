
[app]
title = IPTV App
package.name = iptvapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1
# Přidali jsme konkrétní verze pro stabilitu
requirements = python3,kivy==2.3.0,requests,pyjnius,certifi,openssl

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# TATO ŘÁDKA JE KLÍČOVÁ - opravuje chybu s SDLActivity patchem
p4a.branch = develop

[buildozer]
log_level = 2
