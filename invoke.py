# coding=utf-8
import re
##import sys
##filename = sys.argv[1]
rFilename = "mytest.smali"
wFilename = "myresult.dot"
fRead  = open(rFilename, "r")
fWirte = open(wFilename, "w")
flag = 0		##标记状态
mystring = ''	##最终要写入的string
myclass  = ''	##类名
mysuper  = ''	##父类名
mysource = ''	##来源文件
method   = ''	##函数名
###读文件前三行获取相关信息
count = 0
while (count < 3):
	line = fRead.readline()
	if count == 0:
		getstr = re.findall(r'^.class.*?([^ ]*?)$',line)
		myclass = getstr[0]
		mystring += getstr[0]+'\n'
	elif count ==1:
		getstr = re.findall(r'^.super.*?([^ ]*?)$',line)
		mysuper = getstr[0]
		mystring += getstr[0]+'\n'
	elif count ==2:
		getstr = re.findall(r'^.source.*?([^ ]*?)$',line)
		if len(getstr)!=0:		##有可能没有
			mysource = getstr[0]
			mystring += getstr[0]+'\n'
	count += 1
print mystring

while True:
	line = fRead.readline()
	if line:
		if flag == 0:		##在method体外
			getstr = re.findall(r'^.method.*?([^ ]*?)$',line)
			if len(getstr)!=0:
				method = getstr[0]
				flag = 1
				print method
		if flag == 1:		##在method体内
			getstr = re.findall(r'.end method$',line)
			if len(getstr) != 0:
				method = ''
				flag = 0
				continue
			getstr = re.findall(r'invoke.*?([^ ]*?)$',line)
			if len(getstr) != 0:
				print '	'+getstr[0]
				continue
			getstr = re.findall(r' :(.*?)',line)
			
			
	else:
		break
		
fRead.close()
fWirte.close()