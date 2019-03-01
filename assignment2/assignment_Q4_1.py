#!/usr/bin/python
# _*_ coding:utf-8 _*_

import nltk
import re
import os.path
from nltk.corpus import wordnet as wn
from itertools import product

def open_file(filepath):
    with open(filepath,"r") as f:
        return [re.split("\s+",line.rstrip('\n')) for line in f]

sample = open_file("sim_data/SimLex999-100.txt")
word1 = []
word2 = []
old_simlarity = []
del sample[0]

for i in sample:
    word1.append(i[0])
    word2.append(i[1])
    old_simlarity.append(i[2])

temp = []

count = 0
for j in word1:
    w1 = [j]
    w2 = [word2[count]]
    word_sim_list1 = set(s for word in w1 for s in wn.synsets(word))
    word_sim_list2 = set (s for word in w2 for s in wn.synsets(word))
    if word_sim_list1 and word_sim_list2:
        fittest = max((wn.path_similarity(s1,s2) or 0.00,s1,s2) for s1,s2 in product(word_sim_list1,word_sim_list2))
        temp.append(fittest[0])
    count += 1

if os.path.exists("BioSim-100-predicted.txt"):
    f = open("BioSim-100-predicted.txt","w")
else:
    f = open("BioSim-100-predicted.txt","x")
    f = open("BioSim-100-predicted.txt","w")


index = 0
update_prediction = "word1\tword2\tGoldSimilarity\tWordNetSimiliarity\n"
for i in temp:
    update_prediction += (word1[index])
    update_prediction += "\t"
    update_prediction += (word2[index])
    update_prediction += "\t"
    update_prediction += (old_simlarity[index])
    update_prediction += "\t"
    update_prediction += str(i)
    update_prediction += "\n"
    index += 1

print(update_prediction)
f.write(update_prediction)
f.close()