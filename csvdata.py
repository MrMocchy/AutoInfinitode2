import sys
import csv
import hotkeys
from control import error


#アルゴリズムから由来、一度の操作の単位
class Algo:
	line:int
	name:str
	pos:tuple
	hotkey:tuple
	cate:str
	curLoop:int
	maxLoop:int
	def __init__(self,line,name,pos,cate,hotkey,curLoop=None,maxLoop=None):
		self.line=line
		self.name=name
		self.pos=pos
		self.cate=cate
		self.hotkey=hotkey
		self.curLoop=curLoop
		self.maxLoop=maxLoop
	
	#Algoの内容を表示
	def print(self):
		string=f"{self.line+1:3} {self.name:10} "
		if self.curLoop!=None:
			string+=f"({self.curLoop:2}/{self.maxLoop:2}) "
		else:
			string+="        "
		string+=f"({self.pos[0]:2},{self.pos[1]:2}) {self.cate} {self.hotkey}"
		print(string)

#Algoのリスト。これをmainでループする。
algos:list[Algo]=[]

#コマンドライン引数でステージを指定
stage = sys.argv[1]


"""cat:category:カテゴリ名称の一覧
s:system:このプログラム側への命令。
g:game:ポーズとかのゲーム自体への命令。
t:TOWER
m:MODIFIRE
d:dig:MINER(modifireとの文字かぶり)
u:upgrade
a:abililty
"""

#csvを読み込んでAlgoのリストを作成
with open(f"csv/{stage}.csv","r") as file:
	reader = csv.reader(file)
	
	line = [row for row in reader]

	for lineNo in range(line.__len__()):
		l=line[lineNo]
		if l == []:
			continue
		if not hotkeys.dic.__contains__(l[0]):
			error(f"line {lineNo+1} : \"{l[0]}\" is not defined  (csv/{stage}.csv)")
		if l.__len__() > 2:
			#posありのとき
			pos=(int(l[1]),int(l[2]))
		elif l.__len__()==2:
			#posなしでoptionありのとき
			l.__add__(["",l[1]])
		if l.__len__() > 3:
			#オプションがある時
			if hotkeys.dic[l[0]][0]=="u":
				for i in range(int(l[3]) if hotkeys.dic[l[0]][0]=="u" else int(l[3])):
					algos.append(Algo(line=lineNo,name=l[0],pos=pos,cate=hotkeys.dic[l[0]][0],hotkey=hotkeys.dic[l[0]][1:],curLoop=i,maxLoop=int(l[3])))
			elif hotkeys.dic[l[0]][0]=="t":
				algos.append(Algo(line=lineNo,name=l[0],pos=pos,cate=hotkeys.dic[l[0]][0],hotkey=hotkeys.dic[l[0]][1:]))
				algos.append(Algo(line=lineNo,name=f"ability{l[3]}",pos=pos,cate="a",hotkey=hotkeys.dic[f"ability{l[3]}"][1:]))
			elif hotkeys.dic[l[0]][0]=="a":
				algos.append(Algo(line=lineNo,name=f"ability{l[3]}",pos=pos,cate="a",hotkey=hotkeys.dic[f"ability{l[3]}"][1:]))
			continue
		algos.append(Algo(line=lineNo,name=l[0],pos=pos,cate=hotkeys.dic[l[0]][0],hotkey=hotkeys.dic[l[0]][1:]))

#読み込んだリストを表示
if __name__ == "__main__":
	for a in algos:
		a.print()


print("import finished : "+__name__)