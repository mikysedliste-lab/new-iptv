[app]
# (str) Název tvé aplikace
title = IPTV Master v30

# (str) Název balíčku (bez mezer, jen tečky a malá písmena)
package.name = iptv_master

# (str) Doména balíčku (např. org.tvojejmeno)
package.domain = org.iptv

# (str) Zdrojový kód (tečka znamená aktuální složku, kde je main.py)
source.dir = .

# (list) Přípony souborů, které se mají zahrnout
source.include_exts = py,png,jpg,kv,atlas

# (str) Verze aplikace
version = 30.5

# (list) Požadavky na knihovny (zde jsou všechny, co jsi měl v Colabu)
requirements = python3,kivy==2.2.1,requests,pyjnius,certifi,openssl,urllib3,idna,chardet

# (str) Orientace obrazovky
orientation = portrait

# (bool) Indikuje, zda má být aplikace celoobrazovková
fullscreen = 0

# (list) Oprávnění pro Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# (int) Android API (33 je pro moderní mobily ideální)
android.api = 33

# (int) Minimální verze Androidu (21 = Android 5.0+)
android.minapi = 21

# (str) Architektura (arm64-v8a je pro 99 % dnešních mobilů)
android.archs = arm64-v8a

# (bool) Povolit AndroidX (důležité pro stabilitu)
android.enable_androidx = True

# (str) Log level (2 = debug, uvidíme všechno)
log_level = 2

# (bool) Automaticky přijmout licence
android.accept_sdk_license = True

[buildozer]
# (int) Log level
log_level = 2
