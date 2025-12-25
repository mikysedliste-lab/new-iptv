[app]
title = IPTV Master v30
package.name = iptv_master
package.domain = org.iptv
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 30.5
requirements = python3,kivy==2.2.1,requests,pyjnius,certifi,openssl,urllib3,idna,chardet
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# Tato řádka je klíčová pro opravu té chyby s "patch"
p4a.branch = master

log_level = 2

[buildozer]
log_level = 2
