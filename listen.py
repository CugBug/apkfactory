# -*- coding: utf-8 -*- # 
import pyHook    
import pythoncom
import win32api
import win32con
import time
import threading
def onMouseEvent(event): 
    
	# ��������¼�     
	print "MessageName:",event.MessageName     
	print "Message:", event.Message     
	print "Time:", event.Time     
	print "Window:", event.Window     
	print "WindowName:", event.WindowName     
	print "Position:", event.Position     
	print "Wheel:", event.Wheel     
	print "Injected:", event.Injected           
	print"---"
  
	# ���� True �Ա㽫�¼����������������     
	# ע�⣬���������� False ��������¼�����ȫ������     
	# Ҳ����˵�����꿴�����Ὡ���Ƕ����ƺ�ʧȥ��Ӧ��     
	return True
 
def onKeyboardEvent(event):
	# ���������¼�     
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
		#win32api.keybd_event(87,17,win32con.KEYEVENTF_KEYUP,0) #�ͷŰ���
	return True 
def mythread():
	#win32api.keybd_event(49,2,0,0)	##1
	win32api.keybd_event(49,2,win32con.KEYEVENTF_KEYUP,0) #�ͷŰ���
	##time.sleep(0.1)
	win32api.keybd_event(87,17,0,0)	##w
	win32api.keybd_event(87,17,win32con.KEYEVENTF_KEYUP,0) #�ͷŰ���
	
def main():     
	# ����һ�������ӡ��������     
	hm = pyHook.HookManager()      
	# �������м����¼�     
	hm.KeyDown = onKeyboardEvent     
	# ���ü��̡����ӡ�     
	hm.HookKeyboard()    
	# ������������¼�     
	#hm.MouseAll = onMouseEvent     
	# ������ꡰ���ӡ�     
	#hm.HookMouse()      
	# ����ѭ�����粻�ֶ��رգ�����һֱ���ڼ���״̬     
	pythoncom.PumpMessages()

if __name__ == "__main__":     
	main()