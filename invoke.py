# coding=utf-8
import re
import os
import sys
def PrintBlocks(blocks,jumplist,method):		##将list输出到.dot
	'''
	for xx in blocks:
		print xx
	print jumplist
	print 'return at blocks['+str(Flagreturn)+']'
	'''
	global Flagreturn
	global mydir
	jump = ''
	node = ''
	Nonelist = []
	wFilename = mydir+'\\'+method+'.dot'
	fWirte = open(wFilename, "w")
	fWirte.write('digraph {\n')
	i = 0
	for myNode in blocks:			##写Node信息
		##myNode.replace('\n','|\l')
		if myNode != '#NONE#':
			node += 'Node'+str(i)+' [label="{'+myNode+'\l}"]\n'	##del shape=record,
		else:
			Nonelist.append(i)		##该节点是无用的节点
		i += 1
	node += 'End [shape=record,label="{End\l}"]\n'	##End节点
	fWirte.write(node)
	i = 0
	for myjump in jumplist:			##标记出所有的跳转点
		i += 1
		if myjump[0] == '':
			exec(myjump[1]+'='+str(i))			##节点所代表的下标，比如变量cond_0代表跳转到blocks[3],注意刚好跳转到下一个点，所以应该先+1
												#if myjump[1].find('try_end') == -1:
			jump += 'Node'+str(i-1)+' -> Node'+str(i)+'\n'
			##fWirte.write(jump)
	i = 0
	for myjump in jumplist:			##写跳转流程
		if myjump[0] != '':						##若是跳转的指令
			if myjump[0].find('if') != -1:		##如果是if语句
				jump += 'Node'+str(i)+' -> Node'+str(i+1)+'\n'
				##fWirte.write(jump)
				exec('m = '+myjump[1])
				jump += 'Node'+str(i)+' -> Node'+str(m)+'\n'
				##fWirte.write(jump)
			elif myjump[0].find('goto') != -1:	##如果是goto语句
				exec('m = '+myjump[1])
				jump += 'Node'+str(i)+' -> Node'+str(m)+'\n'
				##fWirte.write(jump)
			elif myjump[0].find('switch') != -1:##如果是switch语句
				exec('m = '+myjump[1])
				for myswitch in m:									##'''有没有跳转到本条switch下面'''
					exec('M = '+myswitch)
					jump += 'Node'+str(i)+' -> Node'+str(M)+'\n'
			elif myjump[0].find('try_end') != -1:##如果是try块的结束
				MyCatchList = trycatchdict[myjump[0]]
				for MyCatch in MyCatchList:
					jump += 'Node'+str(i)+' -> Node'+str(MyCatch)+'\n'
		i += 1
		'''
		if myjump[0].find('switch') != -1:	##如果是switch语句,考虑NONE标志
			jump = 'Node'+str(i)+' -> Node'+str(exec('myjump[1]'))+'\n'
		'''
	###消除return块到其他块的走向，并连上End块，写入到文件中###
	###将NONE消除掉，主要是字符串替换###
	if Flagreturn > -1:
		Beindex = jump.find('Node'+str(Flagreturn)+' ->')
		while Beindex > -1:
			Endindex = jump.find('\n',Beindex)
			jump = jump[:Beindex]+jump[Endindex+1:]
			Beindex = jump.find('Node'+str(Flagreturn)+' ->')
		jump += 'Node'+str(Flagreturn) + ' -> End\n}'
		##print "########"+jump+"########\n"
	for none in Nonelist:
		'''
		##找到所有新node的开始和结束下标
		begin = [0]
		end   = [0]
		index = jump.find('Node'+str(none)+' -> ',end[-1])
		while index > -1:
			begin.append(index)
			end.append(jump.find('\n',begin[-1]))
			index = jump.find('Node'+str(none)+' -> ',end[-1])
		length = len('Node'+str(none)+' -> ')
		listindex = len(begin)-1
		##将新node放到list中,把旧的node ->行删除
		newnode = []
		while listindex > 0:
			mybegin = begin[listindex]
			myend = end[listindex]
			newnode.append(jump[mybegin+length:myend])
			listindex -= 1
			jump = jump[:mybegin]+jump[myend+1:]
		##把旧 -> node行删除并以新node代替之
		toreplace = jump.rfind('-> Node'+str(none)+'\n')
		while toreplace > -1:
			tobegin = jump.rfind('\n',0,toreplace)
			toend = jump.find('\n',toreplace)
			mystr = jump[tobegin:toend]
			myreplace = ''
			for mynewnode in newnode:
				myreplace += mystr.replace('-> Node'+str(none)+'\n','-> '+mynewnode+'\n')
			myreplace = myreplace.replace(mynewnode+' -> '+mynewnode+'\n','')
			print "#myreplace#"+myreplace+"\n######"
			jump = jump[:tobegin]+myreplace+jump[toend:]
			toreplace = jump.rfind('-> Node'+str(none)+'\n',tobegin)
		'''
		
		
		while True:
			begin = jump.find('Node'+str(none)+' -> ')
			if begin > -1:
				length = len('Node'+str(none)+' -> ')
				end = jump.find('\n',begin)
				newnode = jump[begin+length:end]
				#print str(none)+'#turnto'+newnode
				jump = jump[:begin]+jump[end+1:]
				jump = jump.replace('-> Node'+str(none)+'\n','-> '+newnode+'\n')
			else: break
		'''
		start = []
		end = []
		forstart = jump.find(' -> Node'+str(none)+'\n')
		while forstart > -1:
			start.append( jump.rfind('\n',0,forstart) )
			end.append( jump.find('\n',forstart) )
			forstart = jump.find(' -> Node'+str(none)+'\n',end[-1])
		mynewnode = re.findall('Node'+str(none)+' -> (.*?)\n',jump)
		for newnode in mynewnode:
			Begin = jump.find('Node'+str(none)+' -> '+newnode+'\n')
			End = jump.find('\n',Begin)
			jump = jump[:Begin]+jump[End+1:]
			mylen = len(end)-1
			while mylen > -1:
				mystart = start[mylen]
				myend = end[mylen]
				if mystart < 0:
					mystart = 0
				mystr = jump[mystart:myend]
				mystr = mystr.replace('Node'+str(none),newnode)
				mylen -=1
				##print "mystr###"+mystr+"###"
				jump += mystr
		while len(end) > 0:
			myend = end.pop()
			mystart = start.pop()
			jump = jump[:mystart+1]+jump[myend:]
		jump += '\n}'
		'''
	fWirte.write(jump)
	fWirte.close()
	return

filename = sys.argv[1]
rFilename = filename
fRead  = open(rFilename, "r")

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
#print mystring
##print myclass
mydir  = myclass.replace('/','\\')
##myfile = mydir[1:-1]+'.dot'
##IndexOfFile = mydir.rfind('\\')
mydir  = mydir[1:-1]
if not os.path.exists(mydir):
	os.makedirs(mydir)


jumplist = []		##标记着当前APIstring的所在blocks,是一个元组列表[('',''),('',''),('','')]
switchlist = []		##记录所有的switch名称
##numtrycatch = 0	##记录trycatch块的数量
##trylist = []		##try的列表
trycatchdict = {}	##trycatch字典,形式：'try_start_1':['catch_1','catch_2']
while True:
	line = fRead.readline()
	if line:
		if flag == 0:		##在method体外
			getstr = re.findall(r'^.method.*?[<]?([^ ]*?)[>]?[(]',line)
			if len(getstr)!=0:
				method = getstr[0]
				flag = 1
				jumplist = []
				switchlist = []
				trycatchdict = {}
				##PrintBlocks(blocks)
				blocks = []
				Flagreturn = -1
				#print '*************************'
				#print method
		elif flag > 0:		##在method体内
			getstr = re.findall(r'.end method$',line)		##函数结束标记
			if len(getstr) != 0:
				if APIstring == '':
					blocks.append('#NONE#')
				else:
					blocks.append(APIstring)
				PrintBlocks(blocks,jumplist,method)
				APIstring = ''
				method = ''
				flag = 0
				continue
			##若存在switch结构
			if flag > 1:
				i = len(switchlist)-1
				while line.find(switchlist[i]) == -1:
					i -= 1
					if i == -1:
						break
				if line.find(switchlist[i]) > -1:				##读到了switch体，将要记录下switch包含哪些分支
					flag -= 1
					exec(switchlist[i]+'=[]')			##创建全局变量，以switchlist[i]的值命名
					while True:
						line = fRead.readline()
						getstr = re.findall(r' :(.*?$)',line)
						if len(getstr) != 0:
							exec(switchlist[i]+'.append(getstr[0])')	##往switchlist[i]的列表里面加入跳转标记例如:pswitch_0
							continue
						getstr = re.findall(r'.end.*?switch$',line)
						if len(getstr) != 0:
							#print switchlist[i]+"'s branch is:"
							#exec ('print str('+switchlist[i]+')')
							break
					continue
			
			getstr = re.findall(r'invoke.*?([^ ]*?)$',line)	##API调用
			if len(getstr) != 0:
				##print '	'+getstr[0]
				APIstring += getstr[0]+'\n'				## '\n' replace to '|\l'
				continue
			getstr = re.findall(r' +(.*?),? :(.*?$)',line)	##跳转节点
			if len(getstr) != 0:
				if getstr[0][0].find('switch') > -1:		##若是switch跳转
					flag += 1								##标记flag+1，找getstr[0][1]的.packed-switch
					switchlist.append(getstr[0][1])
				if getstr[0][1].find('try') > -1:			##若找到了try块
					strtry = re.findall(r'try_(.+?)_(.+?)$',getstr[0][1])
					#if strtry[0][0] == 'start':				##若找到的是start块
						##trylist.append('try_end_'+strtry[0][1])
					if strtry[0][0] == 'end':					##若找到的是end块
						line = fRead.readline()
						catchstr = re.findall(r'.catch.*?} :(.*?)$',line)
						catchlist = []						##catch的列表
						while len(catchstr) != 0:
							catchlist.append(catchstr[0][0])
							line = fRead.readline()
							catchstr = re.findall(r'.catch.*?} :(.*?)$',line)
						exec('mytry="try_start_'+strtry[0][1]+'"')
						trycatchdict[mytry] = tuple(catchlist)
						#trycatchdict[strtry] = tuple(catchlist)
					##numcatch += 1
					
				##print getstr[0][0]	##第一项if-eqz p1
				##print getstr[0][1]	##第二项cond_0
				if APIstring == '':
					blocks.append('#NONE#')
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