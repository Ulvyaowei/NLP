#!/usr/bin/python
# _*_ coding:utf-8 _*_
import re
import string
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet, stopwords
import os.path
#open file
sample = open ( 'sim_data/text1.txt',encoding="utf8").read ().lower ()
#remove the punctuation
for c in string.punctuation:
    sample = sample.replace ( c, "" )
#the tokens
text1 = word_tokenize ( sample )
text2 = set ( text1 )
#remove the stopwords
text3 = [w for w in text2 if w not in stopwords.words ( "english" )]


# lemmazation
# get tag
def get_wordnet_pos(tag):
    if tag.startswith ( 'J' ):
        return wordnet.ADJ
    elif tag.startswith ( 'V' ):
        return wordnet.VERB
    elif tag.startswith ( 'N' ):
        return wordnet.NOUN
    elif tag.startswith ( 'R' ):
        return wordnet.ADV
    else:
        return None


# lemmatization
# # get the tag of sentence
tagged_sent = pos_tag ( text3 )

wln = nltk.WordNetLemmatizer ()
clear_text = []
for tag in tagged_sent:
    wordnet_pos = get_wordnet_pos ( tag[1] ) or wordnet.NOUN
    clear_text.append ( wln.lemmatize ( tag[0], pos=wordnet_pos ) )

word1 = []
word2 = []
w1 = []
w2 = []
wim = []
hw1 = []
hw2 = []
hwim = []

for i in range ( len ( clear_text ) ):
    #the left word
    word1 = clear_text[i]
    if i == len ( clear_text ) - 1:
        break;
    for j in range ( len ( clear_text[i + 1] ), len ( clear_text ) ):
        #the right word
        word2 = clear_text[j]
        #get the synsets of two words
        for s1 in wordnet.synsets ( word1 ):
            for s2 in wordnet.synsets ( word2 ):
                fittest = []
                #compute the similarity
                similarity = wordnet.path_similarity ( s1, s2 )
                if similarity is None:
                    similarity = 0
                fittest.append ( similarity )

                #get the hypernyms
                hyn1 = s1.hypernyms()
                hyn2 = s2.hypernyms()
                hyn_word1 = []
                hyn_word2 = []
                if hyn1:
                    hyn1 = hyn1[0].lemma_names()
                    hyn_word1.append(hyn1[0])#get the word
                if hyn2:
                    hyn2 = hyn2[0].lemma_names()
                    hyn_word2.append(hyn2[0])
                if not hyn1:
                    hyn_word2.append ( "None" )#if don not exist,add None
                if not hyn2:
                    hyn_word2.append("None")

                for wh1 in s1.hypernyms():
                    for wh2 in s2.hypernyms():
                        h_fittest = []
                        #compute the similarity
                        h_similarity = wordnet.path_similarity ( wh1, wh2 )
                        if h_similarity is None:
                            h_similarity = 0
                        h_fittest.append ( h_similarity )


        new_fittest = sorted(fittest, reverse=True )[0]
        new_h_fittest = sorted ( h_fittest, reverse=True )[0]
        w1.append(word1)
        w2.append(word2)
        wim.append(new_fittest)
        hw1.append(hyn_word1)
        hw2.append(hyn_word2)
        hwim.append(new_h_fittest)
        print(word1,word2,new_fittest,hyn_word1,hyn_word2,new_h_fittest)
#create the file
if os.path.exists("original-pairs-hypernyms.txt"):
    f = open("original-pairs-hypernyms.txt","w",encoding="utf8")
else:
    f = open("original-pairs-hypernyms.txt","x",encoding="utf8")
    f = open("original-pairs-hypernyms.txt","w",encoding="utf8")

index = 0
update_prediction = "word1\tword2\tWordNetSimiliarity\thyp1\thyp2\tSimilarity2\n"
for k in wim:
    update_prediction += (w1[index])
    update_prediction += '\t'
    update_prediction += (w2[index])
    update_prediction += '\t'
    update_prediction += str(k)
    update_prediction += '\t'
    update_prediction += str((hw1[index]))
    update_prediction += '\t'
    update_prediction += str((hw2[index]))
    update_prediction += '\t'
    update_prediction += str((hwim[index]))
    update_prediction += '\n'
    index += 1
#write into the file
print(update_prediction)
f.write(update_prediction)
f.close()
