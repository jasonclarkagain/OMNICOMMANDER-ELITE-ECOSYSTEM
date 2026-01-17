[app]
title = Omnicommander App
package.name = omniapp
package.domain = org.elite.swarm
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 1

# --- PERMISSIONS ---
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# --- BUILD SETTINGS ---
requirements = python3,kivy==2.0.0rc2,pyjnius
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 0
