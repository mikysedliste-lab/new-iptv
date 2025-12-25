[app]
# (str) Název aplikace
title = IPTV Master v30

# (str) Název balíčku (jen malá písmena a podtržítka)
package.name = iptv_master

# (str) Doména balíčku
package.domain = org.iptv

# (str) Zdrojový adresář (tam, kde je main.py)
source.dir = .

# (list) Přípony souborů, které se mají zahrnout
source.include_exts = py,png,jpg,kv,atlas

# (str) Verze aplikace
version = 30.5

# (list) Požadavky na knihovny (včetně SSL pro IPTV streamy)
requirements = python3,kivy==2.2.1,requests,pyjnius,certifi,openssl,urllib3,idna,chardet

# (str) Orientace
orientation = portrait

# (bool) Fullscreen (nastaveno na 0 pro stabilitu)
fullscreen = 0

# (list) Oprávnění pro Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# (int) Android API (33 = Android 13)
android.api = 33

# (int) Minimální verze Androidu
android.minapi = 21

# (str) Architektura
android.archs = arm64-v8a

# (bool) Povolit AndroidX
android.enable_androidx = True

# (bool) Automatické licence
android.accept_sdk_license = True

# (str) Log level
log_level = 2

[buildozer]
log_level = 2
