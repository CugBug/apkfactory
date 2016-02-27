@echo off
dir %cd%|find ".apk" >appname.txt
for /f  "tokens=1-4" %%a in (appname.txt) do (
echo %%a %%b %%c %%d
call permissions.bat %%d
)
del appname.txt
pause