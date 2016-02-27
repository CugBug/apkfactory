set aa=%1
set bb=%1
echo %aa%
set "bb=%bb:.apk=%"
set "aa=%aa:.apk=_permission.txt%"
if not exist %bb%_info md %bb%_info
aapt d permissions %1 > %cd%\%bb%_info\%aa%
set "aa=%aa:_permission.txt=_cert.txt%"
keytool -list -printcert -jarfile %1 > %cd%\%bb%_info\%aa%
set "aa=%aa:_cert.txt=_%"
aapt dump xmltree %1 AndroidManifest.xml > %aa%
aaptinfo.py %aa%
del %aa%