#!/usr/bin/python
# _*_ coding:utf-8 _*_

from nltk import FreqDist,MLEProbDist,re,word_tokenize


j = open('a01_data/sampledata.vocab.txt')
rawVocbText = 'abc'
l = open('a01_data/sampledata.txt')
rawText = '<s> a a b b c c </s><s> a c b c </s><s> b c c a b </s>'


# Unigram
## unsmoothing
rawtext = rawText.replace('<s>','')
rawtext = rawtext.replace('</s>','')
nopunct_word = word_tokenize(rawtext)
print(nopunct_word)
numberA = nopunct_word.count('a')
numberC = nopunct_word.count('c')
numberUNK = nopunct_word.count('unk')
numberWhole = len(nopunct_word)
possibityA = numberA/numberWhole
possibityC = numberC/numberWhole
possibityUNK = numberUNK/numberWhole
print('---------------- Toy dataset ----------------')
print('=== UNIGRAM MODEL ===')
print('- Unsmoothed -')
print('P(a) is:',possibityA,'P(C) is:',possibityC,'P(UNK) is:',possibityUNK)

## smoothing
def smoothing(rawtext,voctext,str):
    nopunct_word = word_tokenize(rawtext)
    nopunct_voc = word_tokenize(voctext)
    numberWhole = len(nopunct_word)
    numberVoc = len(nopunct_voc)+1#UNK is 1
    numberX = rawText.count(str)
    possibityX = (numberX+1)/(numberWhole+numberVoc)#p=(count(a)+1)/(N+V)
    return possibityX

smoothingA = smoothing(rawtext,rawVocbText,'a')
smoothingB = smoothing(rawtext,rawVocbText,'b')
smoothingC = smoothing(rawtext,rawVocbText,'c')
smoothingUNK = smoothing(rawtext,rawVocbText,'UNK')

print('- Smoothed -')
print('P(a) is:',smoothingA,'P(C) is:',smoothingC,'P(UNK) is:',smoothingUNK)


#Bigram
def count(rawtext,str1,str2):
    rawText = rawtext.replace ( ' ', '' )
    numberX= rawText.count(str1)
    i = 0
    countNumber = 0
    while i < len(rawText):
        if rawText[i] == str1 and rawText[i + 1] == str2:
                countNumber += 1
        i += 1
    possibleBia = countNumber/numberX
    return possibleBia

countAB = count(rawText,'a','b')
countSUNK = count(rawText,'<s>','UNK')
print("=== BIGRAM MODEL === ")
print('- Unsmoothed -')
print('P (b|a) is:',countAB,'P (UNK| <s>) is:',countSUNK,"P(UNK|UNK) has no meaning because count(UNK) is zero")

def biagramSmoothing(rawtext,voctext,str1,str2):
    rawText = rawtext.replace(' ', '')
    numberX = rawText.count(str1)
    nopunct_voc = word_tokenize(voctext)
    i = 0
    countNumber = 0
    while i < len (rawText):
        if rawText[i] == str1 and rawText[i + 1] == str2:
            countNumber += 1
        i += 1
    smooth_possible_Bia = (countNumber+1)/(numberX+len(nopunct_voc)+3)
    return smooth_possible_Bia

countABSM = biagramSmoothing(rawText,rawVocbText,'a','b')
countSUNKSM = biagramSmoothing(rawText,rawVocbText,'<s>','UNK')
countDoubleUNK = biagramSmoothing(rawText,rawVocbText,'UNK','UNK')
print('- Smoothed -')
print('P (b|a) is:',countABSM,'P (UNK| <s>) is:',countSUNKSM,'P(UNK|UNK)) is:',countDoubleUNK)

#comput the possible of sentence
print('== SENTENCE PROBABILITIES ==')
#unigram
pos_sentA = smoothingA*smoothingC*smoothingB

pos_sentB = smoothingA*smoothingC*smoothingB*smoothingUNK

pos_sentC = smoothingA*smoothingB*smoothingUNK*smoothingUNK


#biagram
countSCSM = biagramSmoothing(rawText,rawVocbText,'<s>','c')
countCBSM = biagramSmoothing(rawText,rawVocbText,'c','b')
countBASM = biagramSmoothing(rawText,rawVocbText,'b','a')
countASSM = biagramSmoothing(rawText,rawVocbText,'a','</s>')
pos_sentA_bia = countSCSM*countCBSM*countBASM*countASSM



countSASM = biagramSmoothing(rawText,rawVocbText,'<s>','a')
countABSM = biagramSmoothing(rawText,rawVocbText,'a','b')
countBCSM = biagramSmoothing(rawText,rawVocbText,'b','c')
countCUNKSM = biagramSmoothing(rawText,rawVocbText,'c','UNK')
countUNKSSM = biagramSmoothing(rawText,rawVocbText,'UNK','</s>')
pos_sentB_bia = countSASM*countABSM*countBCSM*countCUNKSM*countUNKSSM

countSASM = biagramSmoothing(rawText,rawVocbText,'<s>','a')
countAUNKSM = biagramSmoothing(rawText,rawVocbText,'a','UNK')
countDoubleUNK = biagramSmoothing(rawText,rawVocbText,'UNK','UNK')
countBUNKSM = biagramSmoothing(rawText,rawVocbText,'cUNK','b')
countBSSM = biagramSmoothing(rawText,rawVocbText,'b','</s>')
pos_sentC_bia = countSASM*countAUNKSM*countDoubleUNK*countBUNKSM*countBSSM

print('<s> c b a </s> uprob is',pos_sentA,'biprob is',pos_sentA_bia)
print('<s> a b c d </s> uprob is',pos_sentB,'biprob is',pos_sentB_bia)
print('<s> a d e b </s> uprob is',pos_sentC,'biprob is',pos_sentC_bia)