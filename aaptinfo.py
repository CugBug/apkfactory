# coding=utf-8
import re
import sys
filename = sys.argv[1]
f = open(filename, "r")						##�����ļ���
fs = open(filename+'info\\'+filename+'service.txt',"w")		##����ļ���
fp = open(filename+'info\\'+filename+'provider.txt',"w")
fr = open(filename+'info\\'+filename+'receiver.txt',"w")
fa = open(filename+'info\\'+filename+'activity.txt',"w")
my = ''
myservice  = ''
myprovider = ''
myreceiver = ''
myactivity = ''
flag = 0 #���Ϊfalse
while True:  
	line = f.readline()
	if flag:
		if line:
			getstr = re.findall(r'android:name.*?="(.*?)"',line)
			for ss in getstr:
				my = ''.join(ss)
			if len(my)!=0:
				if flag == 1:
					myservice += my
					myservice += '\n'
				elif flag == 2:
					myprovider += my
					myprovider += '\n'
				elif flag == 3:
					myreceiver += my
					myreceiver += '\n'
				elif flag == 4:
					myactivity += my
					myactivity += '\n'
				##print my
				my = ''
				flag = 0
		else:
			break
	elif line:  
			getstr = re.findall(r'(E: service)',line)
			for ss in getstr:
				my = ''.join(ss)
			if len(my)!=0:
				my = ''
				flag = 1	#service��flag=1
				continue
			getstr = re.findall(r'(E: provider)',line)
			for ss in getstr:
				my = ''.join(ss)
			if len(my)!=0:
				my = ''
				flag = 2	#provider��flag=2
				continue
			getstr = re.findall(r'(E: receiver)',line)
			for ss in getstr:
				my = ''.join(ss)
			if len(my)!=0:
				my = ''
				flag = 3	#receiver��flag=3
				continue
			getstr = re.findall(r'(E: activity)',line)
			for ss in getstr:
				my = ''.join(ss)
			if len(my)!=0:
				my = ''
				flag = 4	#activity��flag=4
				continue
	else:  
			break
fs.write(myservice)
fp.write(myprovider)
fr.write(myreceiver)
fa.write(myactivity)
fs.close()
fp.close()
fr.close()
fa.close()
f.close()
