# coding=utf-8
import re
import sys
filename = sys.argv[1]
f = open(filename+"\\AndroidManifest.xml", "r")
opfname = filename.replace(sys.argv[2],'') ##上层目录的目录名
f1 = open(opfname+sys.argv[2]+'.txt',"w")
my = ''
while True:  
	line = f.readline()
	if line:  
		getstr = re.findall(r'<uses-permission android:name="(.*?)"/>',line)
		for ss in getstr:
			my += ''.join(ss)
			#print my
			my+='\n'
	else:  
		break
f1.write(my)
f1.close()
f.close()
