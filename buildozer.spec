[app]
title = Py Riddle Quest
package.name = pyriddlequest
package.domain = org.codequest
source.dir = .
source.include_exts = py,json,wav,png
version = 2.0.0
requirements = python3==3.12.8,hostpython3==3.12.8,kivy
orientation = portrait
icon.filename = assets/icon.png
fullscreen = 0
android.permissions =
android.api = 35
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
[buildozer]
log_level = 2
warn_on_root = 1
