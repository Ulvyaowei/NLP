# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import nltk
from nltk import re, word_tokenize, FreqDist, MLEProbDist, probability

#open an document
f1 = open('a01_data\sampledata.txt')
dataRaw = f1.read()
f2 = open('a01_data\sampledata.vocab.txt')
vocabRaw = f2.read()

# calculate the frequence distribution
dataRaw_tokens_nopunct = [word for word in word_tokenize(dataRaw) if re.search("\w", word)]

for elem in dataRaw_tokens_nopunct:
    if elem == 's':
        dataRaw_tokens_nopunct.remove(elem)
for elem in dataRaw_tokens_nopunct:
    if elem == '/s':
        dataRaw_tokens_nopunct.remove(elem)
dataRaw_fdist = FreqDist(dataRaw_tokens_nopunct)
##xx = dataRaw_fdist.most_common()
vocabRaw_tokens_nopunct = [word for word in word_tokenize(vocabRaw) if re.search("\w", word)]

# calculate the possibility distribution
dataRaw_pdist = MLEProbDist(dataRaw_fdist)
#yy = [(x, dataRaw_pdist.prob(x)) for x in dataRaw_pdist.samples()]
#yy =(aa, dataRaw_pdist.prob(aa))

# print possibility of word
wordPos = [(x, dataRaw_pdist.prob(x)) for x in vocabRaw_tokens_nopunct]

# print possibility of UNK
KPos = 0
for y in vocabRaw_tokens_nopunct:
    KPos += dataRaw_pdist.prob(y)
UNKPos = [('UNK',(1 - KPos))]

wordPos.append(UNKPos[0])
#print(wordPos)
#print('UNK, ',UNKPos)

# after smoothing
_Pa = (dataRaw_fdist.get('a') + 1) / (len(dataRaw_tokens_nopunct) + len(vocabRaw_tokens_nopunct) + 1)
_Pb = (dataRaw_fdist.get('b') + 1) / (len(dataRaw_tokens_nopunct) + len(vocabRaw_tokens_nopunct) + 1)
_Pc = (dataRaw_fdist.get('c') + 1) / (len(dataRaw_tokens_nopunct) + len(vocabRaw_tokens_nopunct) + 1)
_Punk = 1 - _Pa - _Pb - _Pc
_Pa, _Pb, _Pc, _Punk

# calculate the bi_gram
s1 = '<s>'
s2 = '</s>'
Know = vocabRaw_tokens_nopunct[0] + vocabRaw_tokens_nopunct[1] + vocabRaw_tokens_nopunct[2] 
vocabRaw_tokens_nopunct.append("[^"+ Know +"]")
vocabRaw_tokens_nopunct.append(s1)
Px_a = [0.0, 0.0, 0.0, 0.0, 0.0]
Px_b = [0.0, 0.0, 0.0, 0.0, 0.0]
Px_c = [0.0, 0.0, 0.0, 0.0, 0.0]
Px_UNK = [0.0, 0.0, 0.0, 0.0, 0.0]
Px_s = [0.0, 0.0, 0.0, 0.0, 0.0 ]
Ps_x = [0.0, 0.0, 0.0, 0.0, 0.0 ]

for i in range(0, 5):
    Px_a[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[0] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) / len(re.findall(vocabRaw_tokens_nopunct[0], dataRaw))
    Px_b[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[1] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) / len(re.findall(vocabRaw_tokens_nopunct[1], dataRaw))
    Px_c[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[2] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) / len(re.findall(vocabRaw_tokens_nopunct[2], dataRaw))
    Px_UNK[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[3] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) / len(re.findall(vocabRaw_tokens_nopunct[3], dataRaw))
    Px_s[i] = len(re.findall(s1 + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) / len(re.findall(vocabRaw_tokens_nopunct[4], dataRaw))
    
    Ps_x[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[i] + " " + s2, dataRaw)) / len(re.findall(vocabRaw_tokens_nopunct[i], dataRaw))
    
#print(Px_a, "\n", Px_b, "\n", Px_c, "\n", Px_UNK, "\n", Px_s, "\n", Ps_x)

del Px_a[-1]
del Px_b[-1]
del Px_c[-1]
del Px_UNK[-1]
del Px_s[-1]
Px_a.append(Ps_x[0])
Px_b.append(Ps_x[1])
Px_c.append(Ps_x[2])
Px_UNK.append(Ps_x[3])
Px_s.append(Ps_x[4])

#print(Px_a)
#print(Px_b)
#print(Px_c)
#print(Px_UNK)
#print(Px_s)

#after smoothing
_Px_a = [0.0, 0.0, 0.0, 0.0, 0.0]
_Px_b = [0.0, 0.0, 0.0, 0.0, 0.0]
_Px_c = [0.0, 0.0, 0.0, 0.0, 0.0]
_Px_UNK = [0.0, 0.0, 0.0, 0.0, 0.0]
_Px_s = [0.0, 0.0, 0.0, 0.0, 0.0 ]
_Ps_x = [0.0, 0.0, 0.0, 0.0, 0.0 ]

for i in range(0, 5): 
    _Px_a[i] = (len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[0] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) + 1) / (len(re.findall(vocabRaw_tokens_nopunct[0], dataRaw)) + 5)
    _Px_b[i] = (len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[1] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) + 1) / (len(re.findall(vocabRaw_tokens_nopunct[1], dataRaw)) + 5)
    _Px_c[i] = (len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[2] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) + 1) / (len(re.findall(vocabRaw_tokens_nopunct[2], dataRaw)) + 5)
    _Px_UNK[i] = (len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[3] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) + 1) / (len(re.findall(vocabRaw_tokens_nopunct[3], dataRaw)) + 5)
    _Px_s[i] = (len(re.findall(s1 + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, dataRaw)) + 1) / (len(re.findall(vocabRaw_tokens_nopunct[4], dataRaw)) + 5)

    _Ps_x[i] = (len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[i] + " " + s2, dataRaw)) + 1) / (len(re.findall(vocabRaw_tokens_nopunct[i], dataRaw)) + 5)
    
    
#print(Px_a, "\n", Px_b, "\n", Px_c, "\n", Px_UNK, "\n", Px_s, "\n", Ps_x)

del _Px_a[-1]
del _Px_b[-1]
del _Px_c[-1]
del _Px_UNK[-1]
del _Px_s[-1]
_Px_a.append(_Ps_x[0])
_Px_b.append(_Ps_x[1])
_Px_c.append(_Ps_x[2])
_Px_UNK.append(_Ps_x[3])
_Px_s.append(_Ps_x[4])

#print(_Px_a)
#print(_Px_b)
#print(_Px_c)
#print(_Px_UNK)
#print(_Px_s)

#open an document
f3 = open('a01_data\sampletest.txt')
testRaw = f3.read()
f2 = open('a01_data\sampledata.vocab.txt')
_vocabRaw = f2.read()

# calculate the frequence distribution
testRaw_tokens_nopunct = [word for word in word_tokenize(testRaw) if re.search("\w", word)]

for elem in testRaw_tokens_nopunct:
    if elem == 's':
        testRaw_tokens_nopunct.remove(elem)
for elem in testRaw_tokens_nopunct:
    if elem == '/s':
        testRaw_tokens_nopunct.remove(elem)
testRaw_fdist = FreqDist(testRaw_tokens_nopunct)
##xx = dataRaw_fdist.most_common()
_vocabRaw_tokens_nopunct = [word for word in word_tokenize(_vocabRaw) if re.search("\w", word)]

# calculate the possibility distribution
testRaw_pdist = MLEProbDist(testRaw_fdist)
#yy = [(x, dataRaw_pdist.prob(x)) for x in dataRaw_pdist.samples()]
#yy =(aa, dataRaw_pdist.prob(aa))

# print possibility of word
test_wordPos = [(x, testRaw_pdist.prob(x)) for x in _vocabRaw_tokens_nopunct]

# print possibility of UNK
_KPos = 0
for y in _vocabRaw_tokens_nopunct:
    _KPos += testRaw_pdist.prob(y)
_UNKPos = [('UNK',(1 - _KPos))]
test_wordPos.append(_UNKPos[0])

#print(test_wordPos)

# unigram
Ps_w1 = test_wordPos[0][1] * test_wordPos[1][1] * test_wordPos[2][1]
Ps_w2 = test_wordPos[0][1] * test_wordPos[1][1] * test_wordPos[2][1] * test_wordPos[2][1] * test_wordPos[2][1]
Ps_w3 = test_wordPos[2][1] * test_wordPos[1][1] * test_wordPos[0][1]
Ps_w4 = test_wordPos[0][1] * test_wordPos[1][1] * test_wordPos[2][1] * test_wordPos[3][1]
Ps_w5 = test_wordPos[0][1] * test_wordPos[3][1] * test_wordPos[3][1] * test_wordPos[1][1]

#print(Ps_w1,Ps_w2,Ps_w3,Ps_w4,Ps_w5)

# bigram

vocabRaw_tokens_nopunct.remove(s1)
testPx_a = [0.0, 0.0, 0.0, 0.0]
testPx_b = [0.0, 0.0, 0.0, 0.0]
testPx_c = [0.0, 0.0, 0.0, 0.0]
testPx_UNK = [0.0, 0.0, 0.0, 0.0]

for i in range(0, 4):
    testPx_a[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[0] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, testRaw)) / len(re.findall(vocabRaw_tokens_nopunct[0], testRaw))
    testPx_b[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[1] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, testRaw)) / len(re.findall(vocabRaw_tokens_nopunct[1], testRaw))
    testPx_c[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[2] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, testRaw)) / len(re.findall(vocabRaw_tokens_nopunct[2], testRaw))
    testPx_UNK[i] = len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[3] + " " + vocabRaw_tokens_nopunct[i] + ".*" + s2, testRaw)) / len(re.findall(s1 + ".*" + vocabRaw_tokens_nopunct[3] + ".*" + s2, testRaw))
    
#print(Px_a, "\n", Px_b, "\n", Px_c, "\n", Px_UNK, "\n", Px_s, "\n", Ps_x)



#print(testPx_a,  testPx_b,  testPx_c,  testPx_UNK)

Ps_b1 = testPx_a[1] * testPx_b[2]
Ps_b2 = testPx_a[1] * testPx_b[2] * testPx_c[2] * testPx_c[2]
Ps_b3 = testPx_c[1] * testPx_b[0]
Ps_b4 = testPx_a[1] * testPx_b[2] * testPx_c[3]
Ps_b5 = testPx_a[3] * testPx_UNK[3] * testPx_UNK[1]

#print(Ps_b1,Ps_b2,Ps_b3,Ps_b4,Ps_b5)

print("---------------- Toy dataset ---------------\n")
print("=== UNIGRAM MODEL ===")
print("- Unsmoothed  -")
print("a: %-4.3f  b: %-4.3f  c: %-4.3f  UNK: %-4.3f" % (wordPos[0][1], wordPos[1][1], wordPos[2][1], wordPos[3][1]))
print("\n- Smoothed  -")
print("a: %-4.3f  b: %-4.3f  c: %-4.3f  UNK: %-4.3f" % (_Pa, _Pb, _Pc, _Punk))

print("")

print("=== BIGRAM MODEL ===")
print("- Unsmoothed  -")
print("        a       b       c       UNK     </s>")
print("a       %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (Px_a[0],Px_a[1],Px_a[2],Px_a[3],Px_a[4]))
print("b       %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (Px_b[0],Px_b[1],Px_b[2],Px_b[3],Px_b[4]))
print("c       %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (Px_c[0],Px_c[1],Px_c[2],Px_c[3],Px_c[4]))
print("UNK     %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (Px_UNK[0],Px_UNK[1],Px_UNK[2],Px_UNK[3],Px_UNK[4]))
print("<s>     %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (Px_s[0],Px_s[1],Px_s[2],Px_s[3],Px_s[4]))
#print_bigram_probs(sorted_vocab_keys, toy_dataset_model_unsmoothed)
print("- Smoothed  -")
print("        a       b       c       UNK     </s>")
print("a       %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (_Px_a[0],_Px_a[1],_Px_a[2],_Px_a[3],_Px_a[4]))
print("b       %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (_Px_b[0],_Px_b[1],_Px_b[2],_Px_b[3],_Px_b[4]))
print("c       %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (_Px_c[0],_Px_c[1],_Px_c[2],_Px_c[3],_Px_c[4]))
print("UNK     %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (_Px_UNK[0],_Px_UNK[1],_Px_UNK[2],_Px_UNK[3],_Px_UNK[4]))
print("<s>     %-4.3f   %-4.3f   %-4.3f   %-4.3f   %-4.3f" % (_Px_s[0],_Px_s[1],Px_s[2],Px_s[3],_Px_s[4]))

print("")

print("== SENTENCE PROBABILITIES == ")
print("                       unigram     bigram")
print("<s> a b c </s>:        %-4.3f       %-4.3f " % (Ps_w1,Ps_b1))
print("<s> a b c c c </s>:    %-4.3f       %-4.3f " % (Ps_w2,Ps_b2))
print("<s> c b a </s>:        %-4.3f       %-4.3f " % (Ps_w3,Ps_b3))
print("<s> a b c UNK </s>:    %-4.3f       %-4.3f " % (Ps_w4,Ps_b4))
print("<s> a UNK UNK b </s>:  %-4.3f       %-4.3f " % (Ps_w5,Ps_b5))      
    
print("")