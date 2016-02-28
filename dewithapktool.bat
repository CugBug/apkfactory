@echo off
::set input=%1%
::echo 您输入了参数:%input%
dir %cd%|find ".apk" >appname.txt
for /f  "tokens=1-4" %%i in (appname.txt) do (
echo %%i %%j %%k %%l
call decompile.bat %%l "%1"
call opendir.bat %%l
)
del appname.txt
echo ................
echo All is finished
echo ................
pause