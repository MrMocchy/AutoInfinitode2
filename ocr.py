#import sys
import pyocr
from PIL import Image
#import cv2
import time
#import const
#import inspect
from control import error
import csvdata
import pywinauto
import win32gui
from PIL import ImageGrab
import ctypes
import re
import pyautogui
from PIL import Image

"""
imageDic = {
    "towerpage":"res/towerpage.png",
    "modipage":"res/modipage.png",
    "yes":"res/yes.png",
    "play":"res/play.png",
    "continue":"res/continue.png",
    "newgame":"res/newgame.png",
    "1.2":"res/1.2.png",
}
"""
def imagePass(name):
    return f"res/{name}.png"

#pyocrのセットアップ
tools = pyocr.get_available_tools()
if len(tools) == 0:
    error("No OCR tool found")
tool = tools[0]
#print("Ocr will use tool '%s'" % (tool.get_name()))
langs = tool.get_available_languages()
#print("Available languages: %s" % ", ".join(langs))#0:eng,2:jpn
lang = langs[0]
#print("Ocr will use language: %s" % lang)

def printWindowNames():
    windows = pywinauto.Desktop(backend="uia").windows()
    print([w.window_text() for w in windows])
#window=pywinauto.Desktop(backend='uia')["PC"]
#app=pywinauto.Application().start(r"c:\windows\system32\notepad.exe")
#print(app.windows())

#ウィンドウ取得
hwnd = win32gui.FindWindow(None, 'Infinitode 2')
if hwnd == 0:
    error("Could not find Infinitode2 window")
def setForeground():
    if hwnd:
        if hwnd != win32gui.GetForegroundWindow():
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)
    else:
        error("Infinitode2 window was not found")

if __name__ == "__main__":
    setForeground()

isPause = False

def pauseCheck():
    global isPause
    if pyautogui.locateOnWindow(imagePass("endgame"),"Infinitode 2",grayscale=False,confidence=0.95):
        isPause = True

#ウィンドウが前面にあるか入力前にチェックし、
#なければカウントダウンして終了
def foregroundCheck():
    def waitAndRecheck():
        time.sleep(1)
        if hwnd == win32gui.GetForegroundWindow():
            return True
        return False
    if hwnd != win32gui.GetForegroundWindow():
        if waitAndRecheck(): return
        print("exit in")
        if waitAndRecheck(): return
        print("3...")
        if waitAndRecheck(): return
        print("2..")
        if waitAndRecheck(): return
        print("1.")
        if waitAndRecheck(): return
        error("Infinitode2 window is not foreground")

def getImage(_left,_top,_right,_bottom):
    #1278x718
    foregroundCheck()
    # ウィンドウサイズを取得
    #window_size = win32gui.GetWindowRect(hwnd)
    # ずれを調整
    f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    rect = ctypes.wintypes.RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    f(ctypes.wintypes.HWND(hwnd),ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),ctypes.byref(rect),ctypes.sizeof(rect))
    # 取得したウィンドウサイズでスクリーンショットを撮る
    image = ImageGrab.grab((rect.left+2+_left, rect.top+31+_top, rect.left+2+_right, rect.top+31+_bottom))
    return image

def getTextFromImage(rect,border,show=False) -> str:
    img=getImage(rect[0],rect[1],rect[2],rect[3])
    if img == None:
        return
    #setForeground()
    img=img.convert("RGB")
    size=img.size
    img=img.resize((size[0]*2,size[1]*2))
    size=img.size
    img2=Image.new("RGB",(size[0],size[1]))
    #2値化して精度を上げる
    for x in range(size[0]):
        for y in range(size[1]):
            r,g,b=img.getpixel((x,y))
            if r+g+b > border*3:
                r,g,b=(0,0,0)
            else:
                r,g,b = (255,255,255)
            #img2.putpixel((x*2+1,y),(r,g,b))
            img2.putpixel((x,y),(r,g,b))
    txt = tool.image_to_string(img2,lang,builder=pyocr.builders.TextBuilder(tesseract_layout=6))
    #指定範囲の調整用に切り取った画像と二値化後の画像を並べて表示
    if __name__ == '__main__' or show:
        imgs=Image.new("RGB",(img.size[0]+img2.size[0],img.size[1]))
        imgs.paste(img,(0,0))
        imgs.paste(img2,(img.size[0],0))
        imgs.show()
    return txt


def getTilePos():
    txt = getTextFromImage((1200,0,1278,35),border=50)
    if re.match(r"\d+:\d+",txt):
        pos = txt.split(":")
        return (int(pos[0]),int(pos[1]))
    else:
        return None

def getInt(rect,border,show=False):
    text=getTextFromImage(rect,border,show)
    if re.match(r"\d+$",text):
        return int(text)
    else:
        #print("failed to read int for "+inspect.stack()[1].function+"("+text+")")
        return None

def getCoinNum(show=False):
    return getInt((460,26,550,50),border=130,show=show)

#各キーで押すタワーとかの値段表示の場所
pricePos = {
    "3":(910,400),
    "4":(1000,400),
    "5":(1090,400),
    "6":(1180,400),
    "e":(910,490),
    "r":(1000,490),
    "t":(1090,490),
    "y":(1180,490),
    "d":(910,580),
    "f":(1000,580),
    "g":(1090,580),
    "h":(1180,580),
    "c":(910,670),
    "v":(1000,670),
    "b":(1090,670),
    "n":(1180,670),
}


def clickImage(string):
    box=pyautogui.locateOnWindow(imagePass(string),"Infinitode 2",grayscale=False,confidence=0.95)
    if box:
        pyautogui.moveTo(box.left+box.width/2,box.top+box.height/2)
        pyautogui.leftClick()
        time.sleep(0.3)

def changePage(what):
    clickImage(what+"page")
        
def getUpgradePrice():
    return getInt((1195,590,1260,620),border=200)

def getPuttingPrice(a:csvdata.Algo):
    if a.cate=="t":
        changePage("tower")
        modi=0
    elif a.cate=="m" or a.cate=="d":
        changePage("modi")
        modi=-80
    else:
        error("")
    pos=pricePos[a.hotkey[1]]
    return getInt((pos[0],pos[1]+modi,pos[0]+80,pos[1]+30+modi),border=200)

def getSellPrice():
    return getInt((1170,650,1240,680),border=200)

def getExpLevel():
    text = getTextFromImage((1200,35,1260,60),border=200)
    if re.match(r"L\d+",text):
        return int(text[1:])
    else:
        return None

def getTileName():
    return getTextFromImage((900,35,1100,60),border=200)



if __name__ == '__main__':
    pass
    #print(getTilePos())
    print(getCoinNum())
    #getPrice(const.CRUSHER)
    #getPrice(const.BOUNTY)
    #changePage()
    #print(getUpgradePrice())
    #print(getExpLevel())
    #print(getSellPrice())
    #print(getTileName())
    #getImage(0,0,1278,718).show()

print("import finished : "+__name__)