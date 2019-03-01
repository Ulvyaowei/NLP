#!/usr/bin/python
# _*_ coding:utf-8 _*_


import re
import os.path

#open the file
def open_file(filepath):
    with open(filepath,"r") as f:
        return [re.split("\s+",line.rstrip('\n')) for line in f]


sample = open_file('original-pairs.txt',encoding="utf8")
word1 = []
sim = []
old_similarity = []
word_similarity = []
del sample[0]
#create the map
line_order = {}
for i in sample:
    line_order[i[0] + '  ' + i[1]] = float ( i[2] )
#sort the similarity
result = sorted(line_order.items (), key=lambda item: item[1], reverse=True)[:10]
results = ''
for s in result:
    word1.append(s[0])
    sim.append(s[1])
#create the file
if os.path.exists("top.txt"):
    f = open("top.txt","w",encoding="utf8")
else:
    f = open("top.txt","x",encoding="utf8")
    f = open("top.txt","w",encoding="utf8")

#create the String
update_prediction = "word1\tword2\tGoldSimilarity\tWordNetSimiliarity\n"
index = 0
for i in sim:
    update_prediction += (word1[index])
    update_prediction += "\t"
    update_prediction += str((sim[index]))
    update_prediction += "\n"
    index +=1
#wirte into the file
print(update_prediction)
f.write(update_prediction)
f.close()
