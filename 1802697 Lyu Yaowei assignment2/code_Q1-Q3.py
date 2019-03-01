import nltk
#Question1: 
#Q1/(a) Codes from line 16-25 are added.
q1_grammar = nltk.CFG.fromstring('''
S -> NP VP
VP -> VP PP 
NP -> Det Nom | PropN | NP PP 
Nom -> Adj Nom | N 
VP -> V NP | V S | VP PP 
PP -> P NP 
PropN -> 'Bill'
Det -> 'the' | 'a' | 'an' 
N -> 'bear' | 'squirrel' | 'park' 
Adj -> 'angry' | 'frightened' 
V -> 'chased' | 'saw' | 'put' | 'eats' | 'eat' 
S -> VP                      
P -> 'on'
N -> 'block' | 'table'
NP -> PN
PropN -> 'Bob'
P -> 'in' | 'along'
N -> 'river'
Adj -> 'furry'
N -> 'dog'
V -> 'chase'
''')

#Q1/(b): S1 have two derivations:
s1 = 'put the block on the table'.split()
q1_parser = nltk.ChartParser(q1_grammar)
for tree in q1_parser.parse(s1):
    print(tree)
    tree.draw() 
    
#Q1/(b): S1 have five derivations:
s2 = 'Bob chased a bear in the park along the river'.split()
q1_parser = nltk.ChartParser(q1_grammar)
for tree in q1_parser.parse(s2):
    print(tree)
    tree.draw() 

#Q1/(b): S3 has one derivation:
s3 = 'Bill saw Bob chase the angry furry dog'.split()
q1_parser = nltk.ChartParser(q1_grammar)
for tree in q1_parser.parse(s3):
    print(tree)
    tree.draw() 
    
#------------------------------------------------------------------------------
#Question2:
#Q2/(a): The answer is shown in the report. As there is no need for coding.

#Q2/(b):
#We use Bottom-Up Chart Parser and Earley Chart Parsing for S4 and S5:
q2b_grammar = nltk.CFG.fromstring('''
S -> NP VP
VP -> VP PP | V
NP -> Det Nom | PropN | NNS
Nom -> N 
VP -> V NP | V S | VP PP 
Det -> 'the' | 'a' | 'an' | 'An' |'The'
NNS -> 'dogs'
N -> 'dog' | 'bear' | 'squirrel' |'dogs'
V -> 'eat' | 'eats'
''')

s4 = 'An bear eat an squirrel'.split()
s5 = 'The dogs eats'.split()

#Bottom-Up Chart Parser for S4:
q2_parser_bottumup = nltk.parse.chart.BottomUpChartParser(q2b_grammar, trace=1)
for tree in q2_parser_bottumup.parse(s4):
    print(tree)
#Earley Chart Parsing for S4:
q2_parser_earley = nltk.parse.EarleyChartParser(q2b_grammar, trace=1)
for tree in q2_parser_earley.parse(s4):
    print(tree)
#Bottom-Up Chart Parser for S5:
for tree in q2_parser_bottumup.parse(s5):
    print(tree)
#Earley Chart Parsing for S5:
for tree in q2_parser_earley.parse(s5):
    print(tree)
    
#Explain why the parsers are correct or incorrect:
print('The parsers are incorrect, because the grammars are too simple.\n\
Although they can grammatically recognize the sentences, they fail to parser the sentence by correct singular-plural pair, tense and vowel.')

#Q2/(c)
#Correct 2 correct and 2 incorrect sentenses:
correct1 = 'A boy wins a game'.split()
wrong1 = 'An boy win an game'.split()
correct2 = 'The girl is sleeping'.split()
wrong2 = 'A girls sleep'.split()

#Make Grammar for these 4 sentenses:
q2_c_grammar = nltk.CFG.fromstring('''
S -> NP VP
VP -> VP PP | V
NP -> Det Nom | PropN | NNS
Nom -> N 
VP -> V NP | V S | VP PP | V V
Det -> 'the' | 'a' | 'an' | 'An' |'The' | 'A'
NNS -> 'dogs'
N -> 'girl' |  'girls' | 'boy' | 'game'
V -> 'sleep' | 'sleeping' | 'is' | 'win' | 'wins'
''')

q2_c_grammar_parser = nltk.ChartParser(q2_c_grammar)
#Parser for correct1:
for tree in q2_c_grammar_parser.parse(correct1):
    print(tree)
    tree.draw()
#Parser for correct2:
for tree in q2_c_grammar_parser.parse(correct2):
    print(tree)
    tree.draw()
#Parser for wrong1:
for tree in q2_c_grammar_parser.parse(wrong1):
    print(tree)
    tree.draw()
#Parser for wrong1:
for tree in q2_c_grammar_parser.parse(wrong2):
    print(tree)
    tree.draw()
    
print('For the incorrect sentence, we can make the grammar more complex and more detailed. For example, instead of Det -> ‘a’ | ‘an’, we can turn them into Detnonvowel -> \'a\', Detnvowel -> ‘an’. In this case, if the first letter of a noun is vowel, only ‘an’ can connect with to form a grammar. Similarly, we can make grammar of tense or pronoun more detailed. The following are the revised sentence for the incorrect sentence parsed by more detailed grammar')

#updated detailed grammar for correct1:
q2_c_u1_grammar = nltk.CFG.fromstring('''
S -> NPsg VPsg
VPsg -> VBZ NPsg
NPsg -> Detnonvowel NN
Nom -> N 
Detnonvowel -> 'a' | 'A'
NN -> 'game' |'boy'
VBZ -> 'wins'
''')
#parser for correct1 using updated detailed grammar:
parser_q2_c_u1_grammar = nltk.ChartParser(q2_c_u1_grammar)
for tree in parser_q2_c_u1_grammar.parse(correct1):
    print(tree)
    tree.draw()
#updated detailed grammar for correct2:
q2_c_u2_grammar = nltk.CFG.fromstring('''
S -> NPsg VPsg
VPsg -> VBZsg VBG
NPsg -> Det NN
Nom -> N 
Det -> 'The'
NN -> 'girl'
VBZsg -> 'is'
VBG -> 'sleeping'
''')
#parser for correct2 using updated detailed grammar:
parser_q2_c_u1_grammar = nltk.ChartParser(q2_c_u2_grammar)
for tree in parser_q2_c_u1_grammar.parse(correct2):
    print(tree)
    tree.draw()
    
#-----------------------------------------------------------------------------
#Question3:
#Q3/(a):
# Make a grammar for s6:
s6_grammar = nltk.CFG.fromstring('''
S -> NP VP
VP -> VP PP 
NP -> Det Nom | NP PP | NNS 
Nom -> N 
VP -> V NP | V S | VP PP 
PP -> P NP 
NP -> Pronoun
Pronoun -> 'He'
P -> 'in' | 'with'
Det -> 'the' | 'some'
V -> 'eats'
NNS -> 'pasta' 
N ->  'anchovies' | 'restaurant'
''')

#Parser s6:
#Five interpretations for s6 are shown in the report
s6 = 'He eats pasta with some anchovies in the restaurant'.split()
s6_parser = nltk.ChartParser(s6_grammar)
for tree in s6_parser.parse(s6):
    print(tree)
    tree.draw() 

# Make a grammar for s7:
s7_grammar = nltk.CFG.fromstring('''
S -> NP VP
VP -> VP PP 
NP -> Det Nom | NP PP | NNS 
Nom -> N 
VP -> V NP | V S | VP PP 
PP -> P NP 
NP -> Pronoun
Pronoun -> 'He'
P -> 'in' | 'with'
Det -> 'the' | 'some' | 'a'
V -> 'eats'
NNS -> 'pasta' 
N ->  'fork' | 'restaurant'
''')

#Parser s7:
#Five interpretations for s7 are shown in the report
s7 = 'He eats pasta with a fork in the restaurant'.split()
s7_parser = nltk.ChartParser(s7_grammar)
for tree in s7_parser.parse(s7):
    print(tree)
    tree.draw()

#Q3/(b):
#Earley Chart Parser for s6:
parser_s6_earley = nltk.parse.earleychart.EarleyChartParser(s6_grammar, trace=1)
for tree in parser_s6_earley.parse(s6):
    print(tree)
#Earley Chart Parser for s7:
parser_s7_earley = nltk.parse.earleychart.EarleyChartParser(s7_grammar, trace=1)
for tree in parser_s7_earley.parse(s7):
    print(tree)

#Shift Reduce Parser for s6:
s6_sr_grammar = nltk.CFG.fromstring('''
S -> Pronoun VP | S PP
NP -> Det N | NP PP | NNS PP 
VP -> V NP
PP -> P NP 
Pronoun -> 'He'
P -> 'in' | 'with'
Det -> 'the' | 'some'
V -> 'eats'
NNS -> 'pasta' 
N ->  'anchovies' | 'restaurant'
''')

s6_sr = nltk.ShiftReduceParser(s6_sr_grammar,trace=2)
for tree in s6_sr.parse(s6):
    print(tree)

#Shift Reduce Parser for s7:
s7_sr_grammar = nltk.CFG.fromstring('''
S -> Pronoun VP | S PP
NP -> Det N | NP PP 
VP -> V NNS | VP PP
PP -> P NP 
Pronoun -> 'He'
P -> 'in' | 'with'
Det -> 'the' | 'some' | 'a'
V -> 'eats'
NNS -> 'pasta' 
N ->  'fork' | 'restaurant'
''')
s7 = 'He eats pasta with a fork in the restaurant'.split()
sr = nltk.ShiftReduceParser(s7_sr_grammar,trace=2)
for tree in sr.parse(s7):
    print(tree)