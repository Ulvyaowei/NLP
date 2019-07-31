import urllib
import nltk
from nltk import pos_tag
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
import ssl


# Abstract the information from url
url = 'https://www.theguardian.com/music/2018/oct/19/while-my-guitar-gently-weeps-beatles-george-harrison'
ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
content = soup.find("div",class_='content__main-column content__main-column--article js-content-main-column ')

# get tokens
text_nopunct = [word.lower() for word in content.get_text().split()]
print('This text contains tokens before lemmatization:\n',len(text_nopunct))
# get types
print('This text contains types before lemmatization：\n',len(set(text_nopunct)))


#get tag
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return  wordnet.ADV
    else:
        return None

# lemmatization
# # get the tag of sentence
tagged_sent = pos_tag(text_nopunct)

wln = nltk.WordNetLemmatizer()
lemmas_sent = []
for tag in tagged_sent:
    wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
    lemmas_sent.append(wln.lemmatize(tag[0], pos = wordnet_pos))

print('This text contains tokens after lemmatization:')
print(len(lemmas_sent))
print('This text contains types after lemmatization:')
print(len(set(lemmas_sent)))

print(tagged_sent)


