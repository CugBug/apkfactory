@echo off
set a=%1
set "a=%a:.apk=%"
keytool -printcert -file %a%/original/META-INF/*.RSA >%a%/%a%_Cert.txt
service.py %cd%\%a% %a%
::exit