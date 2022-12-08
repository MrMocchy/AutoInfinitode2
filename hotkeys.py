import csv

#"name"="cate","hotkey[0]","hotley[1]"
dic={}

#csvからホットキーを読み込んで辞書型を作成
with open("csv/hotkeys.csv","r") as file:
	reader = csv.reader(file)
	lines = [row for row in reader]
	for i,line in enumerate(lines):
		if i == 0:
			continue
		dic[line[0]]=(line[1],line[2],line[3])

if __name__=="__main__":
	print(dic)

print("import finished : "+__name__)