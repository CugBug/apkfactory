@echo off
::set input=%1%
::echo �������˲���:%input%
dir %cd%|find ".apk" >appname.txt
for /f  "tokens=1-4" %%i in (appname.txt) do (
echo %%i %%j %%k %%l
call decompile.bat %%l "%1"
start opendir.bat %%l
)
echo ........
echo finished
echo ........
pause