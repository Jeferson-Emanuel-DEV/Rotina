[app]
title = Minha Rotina
package.name = minharotina
package.domain = org.rotina

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js

version = 1.0.0

requirements = python3,flask,plyer,android

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, POST_NOTIFICATIONS

[buildozer]
log_level = 2
warn_on_root = 1