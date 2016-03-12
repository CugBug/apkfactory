# -*- coding: utf-8 -*- # 
import pyHook    
import pythoncom
import win32api
import win32con
import time
import threading
def onMouseEvent(event): 
    
	# 监听鼠标事件     
	print "MessageName:",event.MessageName     
	print "Message:", event.Message     
	print "Time:", event.Time     
	print "Window:", event.Window     
	print "WindowName:", event.WindowName     
	print "Position:", event.Position     
	print "Wheel:", event.Wheel     
	print "Injected:", event.Injected           
	print"---"
  
	# 返回 True 以便将事件传给其它处理程序     
	# 注意，这儿如果返回 False ，则鼠标事件将被全部拦截     
	# 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了     
	return True
 
def onKeyboardEvent(event):
	# 监听键盘事件     
	print "MessageName:", event.MessageName     
	print "Message:", event.Message     
	print "Time:", event.Time     
	print "Window:", event.Window     
	print "WindowName:", event.WindowName     
	print "Ascii:", event.Ascii, chr(event.Ascii)     
	print "Key:", event.Key     
	print "KeyID:", event.KeyID     
	print "ScanCode:", event.ScanCode     
	print "Extended:", event.Extended     
	print "Injected:", event.Injected     
	print "Alt", event.Alt     
	print "Transition", event.Transition     
	print "---"      
	if event.KeyID == 49:
		t = threading.Thread(target=mythread)
		t.start()
		#win32api.keybd_event(87,17,0,0)	##w
		#win32api.keybd_event(87,17,win32con.KEYEVENTF_KEYUP,0) #释放按键
	return True 
def mythread():
	#win32api.keybd_event(49,2,0,0)	##1
	win32api.keybd_event(49,2,win32con.KEYEVENTF_KEYUP,0) #释放按键
	##time.sleep(0.1)
	win32api.keybd_event(87,17,0,0)	##w
	win32api.keybd_event(87,17,win32con.KEYEVENTF_KEYUP,0) #释放按键
	
def main():     
	# 创建一个“钩子”管理对象     
	hm = pyHook.HookManager()      
	# 监听所有键盘事件     
	hm.KeyDown = onKeyboardEvent     
	# 设置键盘“钩子”     
	hm.HookKeyboard()    
	# 监听所有鼠标事件     
	#hm.MouseAll = onMouseEvent     
	# 设置鼠标“钩子”     
	#hm.HookMouse()      
	# 进入循环，如不手动关闭，程序将一直处于监听状态     
	pythoncom.PumpMessages()

if __name__ == "__main__":     
	main()