# coding=utf-8
import re
import sys
filename = sys.argv[1]
f = open(filename+"\\AndroidManifest.xml", "r")
s = open(filename+"\\res\\values\\strings.xml","r")
s1 = open(filename+"\\"+sys.argv[2]+'_Strings.txt',"w")
##	opfname = filename.replace(sys.argv[2],'') ##上层目录的目录名
f1 = open(filename+"\\"+sys.argv[2]+'_Service.txt',"w") ##opfname改成filename+"\\",下同
f2 = open(filename+"\\"+sys.argv[2]+'_Permission.txt',"w")
f3 = open(filename+"\\"+sys.argv[2]+'_Activity.txt',"w")
f4 = open(filename+"\\"+sys.argv[2]+'_Provider.txt',"w")
f5 = open(filename+"\\"+sys.argv[2]+'_Receiver.txt',"w")
mystrings = ''
mypermission = ''
myservice = ''
myactivity = ''
myprovider = ''
myreceiver = ''
try:
	s_all = s.read( )
	getstr = re.findall(r'<string.*?>(.*?)</string>',s_all,re.S)
	for xx in getstr:
		mystrings += ''.join(xx)
		mystrings += '\n'
finally:
	s.close( )
while True:  
	line = f.readline()
	if line:  
		getstr = re.findall(r'<service.*?android:name="(.*?)"',line)
		for xx in getstr:
			myservice += ''.join(xx)
			#print myservice
			myservice+='\n'
			break
		getstr = re.findall(r'<(uses-permission|permission) android:name="(.*?)"/>',line)
		for xx in getstr:
			mypermission += ''.join(xx)
			mypermission+='\n'
			break
		getstr = re.findall(r'<activity.*?android:name="(.*?)"',line)
		for xx in getstr:
			myactivity += ''.join(xx)
			myactivity+='\n'
			break
		getstr = re.findall(r'<provider.*?android:name="(.*?)"',line)
		for xx in getstr:
			myprovider += ''.join(xx)
			myprovider+='\n'
			break
		getstr = re.findall(r'<receiver.*?android:name="(.*?)"',line)
		for xx in getstr:
			myreceiver += ''.join(xx)
			myreceiver+='\n'
			break
	else:  
		break
f1.write(myservice)
f2.write(mypermission)
f3.write(myactivity)
f4.write(myprovider)
f5.write(myreceiver)
s1.write(mystrings)
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
s1.close()
f.close()
print "......................"
print sys.argv[2]+" FINISHED!"
print "......................"