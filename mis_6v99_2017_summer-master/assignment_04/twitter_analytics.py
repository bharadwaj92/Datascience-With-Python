#importing libraries of pandas and numpy
import pandas as pd
import requests
import numpy as np
import math
from collections import OrderedDict
#input url from which file is read
inputurl = "http://kevincrook.com/utd/tweets.json"
#the http respose is stored in resp
resp = requests.get(inputurl)
#using pandas to normalize the json data
msgs = pd.io.json.json_normalize(resp.json())
#extracting only the text and language properties of normalized json
temp = msgs[['text','lang']]
#taking only texts which are not null since they are only considered events
temp1 = temp[temp.text.notnull()]
#writing to first file with utf-8 encoding
f = open("twitter_analytics.txt",'w',encoding="utf-8")
#printing number of tweets
print(len(msgs),file=f)
#printing number of tweet events
print(len(temp1),file=f)
#counting frequency of each language
temp3 = temp1.groupby('lang').count()
dct = temp3.to_dict()
#writing the language frequncy to file
freq_dict = dct['text']
for k,v in sorted(freq_dict.items(), key=lambda x: x[1], reverse = True):
    print(",".join([k,str(v)]),file=f)
f.close()
#writing the tweets to another file.
f_t = open(file="tweets.txt", mode="w", encoding="utf-8")
for fr in temp1['text']:
    print(fr,file=f_t)
f_t.close()
