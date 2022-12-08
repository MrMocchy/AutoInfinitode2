#import os
#import subprocess #cmd
import control
import ocr
#import const
#import jdata
import time
import csvdata
import hotkeys



pos=(0,0)

def moveTo(target):
	global pos
	if target==None:
		return
	control.moveBy(target[0]-pos[0],target[1]-pos[1])
	pos=target




saving = 0
bountyNum = 0

#受け取ったAlgoを実行できるかどうかのbool
def canDo(a:csvdata.Algo):
	tile = ocr.getTileName()
	if a.cate == "g":
		return True
	elif ocr.isPause:
		return False
	elif tile == "":
		return False
	#現在のタイルに不適切な行動の判別と、コスト取得
	elif tile == "PLATFORM":
		if not(a.cate=="t" or a.cate=="m"):
			a.print()
			control.error("unable to do \""+a.name+"\" on "+tile)
		price = ocr.getPuttingPrice(a)
	elif tile == "SOURCE":
		if a.cate != "d":
			a.print()
			control.error("unable to do \""+a.name+"\" on "+tile)
		price = ocr.getPuttingPrice(a)
	elif tile=="ROAD" or tile =="BASE" or tile=="PORTAL" or tile=="MUSIC":
		a.print()
		control.error("unable to do \""+a.name+"\" on "+tile)
	elif hotkeys.dic[tile.lower()][0] == "t":
		if a.cate == "a":
			#アビリティはノーコスト
			return True
		elif a.cate != "u":
			a.print()
			control.error("unable to do \""+a.name+"\" on "+tile)
		price = ocr.getUpgradePrice()
	elif hotkeys.dic[tile.lower()][0] == "d":
		if a.cate != "u":
			a.print()
			control.error("unable to do \""+a.name+"\" on "+tile)
		price = ocr.getUpgradePrice()
	#コスト的な実行不可能の判断
	coin = ocr.getCoinNum()
	if price == None:
		return False
	if coin == None:
		return False
	if a.name == "bounty":
		return coin > price*(bountyNum +1)
	if coin-saving-price>0:
		return True
	return False

#預金の効率化用の計算
def recalcBounty(a):
	global saving
	saving = ocr.getPuttingPrice(a)*bountyNum


ocr.setForeground()

#New Game
ocr.clickImage("newgame")
ocr.clickImage("1.2")
time.sleep(0.7)
ocr.clickImage("continue")
ocr.clickImage("yes")
ocr.clickImage("play")


i = -1
while True:
	i+=1
	#ポーズ画面なら処理一時停止
	ocr.pauseCheck()
	if ocr.isPause:
		while True:
			ip = input(">>")
			if ip=="continue":
				control.continueWhilePause()
				ocr.isPause=False
				break
			elif ip=="exit":
				control.trueExit()
	#Algo実行
	if i >= csvdata.algos.__len__():
		break
	a=csvdata.algos[i]
	if a.cate == "s":
		a.print()
		if a.name=="setpos":
			pos = a.pos
			continue
		elif a.name=="finish":
			control.trueExit()
	moveTo(a.pos)
	if canDo(a):
		if a.name == "bounty":
			bountyNum+=1
			recalcBounty(a)
		control.do(a)
	else:
		time.sleep(1)
		i-=1
		continue

control.trueExit()