import os
#import subprocess #cmd
import serial
#import ocr
import time
import pyautogui
import inspect


#シリアル通信のセットアップ
ser = serial.Serial()
#デバイスマネージャでArduinoのポート確認
readlines = os.popen("powershell \"Get-CimInstance Win32_PnPEntity | Where-Object {$_ -like \'*Arduino*\'} | Select-Object Caption\"").readlines()
if readlines == []:
	print("error @ control")
	print("Arduino was not found")
	exit()
PORT = readlines[3][15:-2]
ser.port = PORT
ser.baudrate = 9600       #Arduinoと合わせる
ser.setDTR(False)         #DTRを常にLOWにしReset阻止

ser.open()
print("opened COM port")

#pyautoguiの矢印キーがはじかれるので、Arduinoを介して移動入力
def moveBy(dx,dy):
	string=b""
	if dx<0:
		string+=b"l"*(-dx)
	else:
		string+=b"r"*dx
	if dy<0:
		string+=b"d"*(-dy)
	else:
		string+=b"u"*dy
	ser.write(string)
	time.sleep(0.2*(abs(dx)+abs(dy)))

#後始末して終了
def trueExit():
	ser.close()
	print("closed COM port")
	print("Finished")
	exit()

#エラーメッセージ出して終了
def error(message,exit=True):
	print(f"error @ {inspect.stack()[1].function} (line {str(inspect.stack()[1].lineno)}) @ "+str(inspect.stack()[1].filename.split('\\')[-1]))
	print(message)
	if exit:
		trueExit()


def continueWhilePause():
	import ocr
	ocr.setForeground()
	pyautogui.press("escape")

#指定のAlgoを実行する
def do(a):
	#shiftはpyautoguiでは単体で押下できないのでArduinoで代わりに押す
	if a.hotkey[1] == "shift":
		pyautogui.keyDown(a.hotkey[0])
		ser.write(b"s")
		pyautogui.keyUp(a.hotkey[0])
	else:
		pyautogui.hotkey(a.hotkey[0],a.hotkey[1])
	a.print()
	time.sleep(0.2)


print("import finished : "+__name__)