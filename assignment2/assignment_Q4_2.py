#!/usr/bin/python
# _*_ coding:utf-8 _*_

import re
import nltk
from nltk import word_tokenize,pos_tag
from nltk.corpus import wordnet,stopwords
import os.path
from nltk.stem.wordnet import WordNetLemmatizer


def open_file(filepath):
    with open(filepath,'r') as f:
        return [re.split("\s+",line.rstrip('\n')) for line in f]

sample = open('sim_data/text1.txt',encoding="utf8")
simlarity = []

text = re.sub(r'[^\w\s]','',sample.read())
text = word_tokenize(text.lower())
text1 = set(text)
#lemmazation
text2 = [WordNetLemmatizer().lemmatize(word) for word in text1]
print(text2)
#removing the stop word
clear_text = [w for w in text1 if w not in stopwords.words("english")]
print(len(clear_text))


word1 = []
word2 = []
temp = []
w1 = []
w2 = []
wim = []

for i in range(len(clear_text)):
    word1 = clear_text[i]
    for j in range(len(clear_text)):
        word2 = clear_text[j]
        if word1 == word2:
            continue;
        for s1 in wordnet.synsets(word1):
            for s2 in wordnet.synsets(word2):
                fittest = []
                simialrity  = wordnet.path_similarity( s1, s2 )
                if simialrity is None:
                    simialrity = 0
                fittest.append(simialrity)
        new_fittest = sorted(fittest,reverse=True)[0]
        print(word1, word2, new_fittest)
        w1.append(word1)
        w2.append(word2)
        wim.append(new_fittest)
print(wim)
print(w1)
print(w2)

if os.path.exists("original-pairs.txt"):
    f = open("original-pairs.txt","w")
else:
    f = open("original-pairs.txt","x")
    f = open("original-pairs.txt","w")

index = 0
update_prediction = "word1\tword2\tWordNetSimiliarity\n"
for k in wim:
    print(wim[index])
    print(w1[index])
    print(w2[index])
    update_prediction += (w1[index])
    update_prediction += '\t'
    update_prediction += (w2[index])
    update_prediction += '\t'
    update_prediction += str(k)
    update_prediction += '\n'
    index += 1

print(update_prediction)
f.write(update_prediction)
f.close()


