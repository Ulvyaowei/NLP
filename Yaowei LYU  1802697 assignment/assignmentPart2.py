#!/usr/bin/python
# _*_ coding:utf-8 _*_

import nltk
import urllib
from nltk import re
from bs4 import BeautifulSoup
from urllib import request
import ssl


#Abstract the information from the url
url = input("Enter Your Website:\n")
ssl._create_default_https_context = ssl._create_unverified_context
html = request.urlopen(url).read()
raw = BeautifulSoup(html).get_text()
text_nopunct = [word for word in raw.split()]
print(raw)
raw = raw.replace(' ','')

#Get the telephone number
pattern = re.compile("((\+?55|0)\-?\s?[1-9]{2}\-?\s?[2-9]{1}\d{3,4}\-?\d{4}|(\0?\d{4,5})\s?\d{6}|\0\d{10}|(\+44|0044)\s?\d{10})")
result = pattern.findall(str(html))
i = 0
print("Found a Match:")

print(result[i])

#print(pattern)


