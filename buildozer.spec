[app]

title = Light Calculator
package.name = lightcalculator
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1


[app:android]

android.api = 35
android.minapi = 23
android.ndk = 28c

android.accept_sdk_license = True

android.archs = arm64-v8a

android.allow_backup = True
android.private_storage = True
