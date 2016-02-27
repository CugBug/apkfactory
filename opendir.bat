@echo off
set a=%1
set "a=%a:.apk=%"
::echo %a%
cd %a%
set path=%cd%
cd..
service.py %path% %a%
exit
::start notepad++ "AndroidManifest.xml"
::cd..