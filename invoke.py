# coding=utf-8
import re
##import sys

def PrintBlocks(blocks,jumplist):		##将list输出到.dot
	for xx in blocks:
		print xx
	print jumplist
	global Flagreturn
	print 'return at blocks['+str(Flagreturn)+']'
	
	global fWirte
	fWirte.write('digraph {\n')
	i = 0
	for myNode in blocks:			##写Node信息
		##myNode.replace('\n','|\l')
		node = 'Node'+str(i)+' [label="{'+myNode+'\l}"]\n'	##del shape=record,
		fWirte.write(node)
		i += 1
	node = 'End [shape=record,label="{End\l}"]\n'	##End节点
	fWirte.write(node)
	i = 0
	for myjump in jumplist:			##标记出所有的跳转点
		i += 1
		if myjump[0] == '':
			exec(myjump[1]+'='+str(i))			##节点所代表的下标，比如变量cond_0代表跳转到blocks[3],注意刚好跳转到下一个点，所以应该先+1
	i = 0
	for myjump in jumplist:			##写跳转流程
		if myjump[0] != '':						##若是跳转的指令
			if myjump[0].find('if') != -1:		##如果是if语句
				jump = 'Node'+str(i)+' -> Node'+str(i+1)+'\n'
				fWirte.write(jump)
				exec('M = myjump[1]')
				exec('m = M')
				jump = 'Node'+str(i)+' -> Node'+m+'\n'
				fWirte.write(jump)
			if myjump[0].find('goto') != -1:	##如果是goto语句
				exec('M = myjump[1]')
				exec('m = M')
				jump = 'Node'+str(i)+' -> Node'+m+'\n'
				fWirte.write(jump)
				'''
			if myjump[0].find('switch') != -1:	##如果是switch语句,考虑NONE标志
				jump = 'Node'+str(i)+' -> Node'+str(exec('myjump[1]'))+'\n'
				'''
	jump = 'Node'+str(Flagreturn) + ' -> End\n}'
	fWirte.write(jump)
	return

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
blocks   = []	##记录API流程的列表
APIstring =''	##将写进字典的API字符串

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

jumplist = []		##标记着当前APIstring的所在blocks,是一个元组列表[('',''),('',''),('','')]
while True:
	line = fRead.readline()
	if line:
		if flag == 0:		##在method体外
			getstr = re.findall(r'^.method.*?([^ ]*?)$',line)
			if len(getstr)!=0:
				method = getstr[0]
				flag = 1
				jumplist = []
				##PrintBlocks(blocks)
				blocks = []
				print '*************************'
				print method
		elif flag == 1:		##在method体内
			getstr = re.findall(r'.end method$',line)		##函数结束标记
			if len(getstr) != 0:
				method = ''
				flag = 0
				if APIstring == '':
					blocks.append('NONE')
				else:
					blocks.append(APIstring)
				PrintBlocks(blocks,jumplist)
				APIstring = ''
				continue
			getstr = re.findall(r'invoke.*?([^ ]*?)$',line)	##API调用
			if len(getstr) != 0:
				##print '	'+getstr[0]
				APIstring += getstr[0]+'\n'				## '\n' replace to '|\l'
				continue
			getstr = re.findall(r' +(.*?),? :(.*?$)',line)	##跳转节点
			if len(getstr) != 0:
				##print getstr[0][0]	##第一项if-eqz p1
				##print getstr[0][1]	##第二项cond_0
				if APIstring == '':
					blocks.append('NONE')
				else:
					blocks.append(APIstring)
				APIstring = ''
				jumplist.append(getstr[0])
				continue
			getstr = re.findall(r'return',line)				##return标记
			if len(getstr) != 0:
				Flagreturn = len(blocks)					##return所在的blocks下标
				continue
	else:
		break
fRead.close()
fWirte.close()

'''
每个jumplist包含所有跳转指令
每个blocks包含所有API
将smali代码分成
	blocks
	jumplist
	blocks
	jumplist
	...
	blocks
所以blocks永远都比jumplist多一个
'''