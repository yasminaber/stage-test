import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
from elasticsearch import Elasticsearch
import html2text
import re
import csv
import datetime
from dateutil.parser import parse


url = 'http://www.senat.fr/communiques/'


response = requests.get(url)

print(response)


soup = BeautifulSoup(response.text, "html.parser")

print(soup)


link_tags = soup.find_all(attrs={"class": "link"})

print(link_tags)


datetime.datetime.strptime('19 June 2020', '%d %B %Y')


today = datetime.date.today()
df = pd.DataFrame(columns=['url','date'])

for a_tag in link_tags:
    df = df.append({'url': 'http://www.senat.fr' + a_tag['href'],'date' : today}, ignore_index=True)
print(df)


df.insert(2,'nom','Yasmina')

print(df)


es = Elasticsearch(
    ['c5686723f70adb7b73c6a584e8031453.eu-west-1.aws.found.io'],
    http_auth=('stage-test', 'guwja8-wirCes-jomhyh'),
    scheme="https",
    port=9243,
    
)


for index, row in df.iterrows():
    res=es.index(index='stage-test',id=index+1,body=row.to_json(date_format='iso'))


my_dict = {}



response = requests.get("http://www.senat.fr/presse/cp20200624e.html")
soup = BeautifulSoup(response.text, "html.parser")
link_tags = soup.find_all(attrs={"id": "CP"})

soup = BeautifulSoup(str(link_tags[0]), "html.parser")
link_tags = soup.find_all('p')
text = ''
for str1 in link_tags:
    text = text + str(str1)
    
h = html2text.HTML2Text()
# Ignore converting links from HTML
h.ignore_links = True
h.ignore_emphasis = True


print(h.handle(text))

communique_text_dict = {}
for index, row in df.iterrows():
    link=row['url']
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    link_tags = soup.find_all(attrs={"id": "CP"})
    soup = BeautifulSoup(str(link_tags[0]), "html.parser")
    link_tags = soup.find_all('p')
    text = ''
    for str1 in link_tags:
        text = text + str(str1)
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_emphasis = True
    h.ignore_images = True
    communique_text_dict[link] = h.handle(text)
	
	

acronymes = {}
for key in communique_text_dict:
    acronymes[key] = re.findall("\d*[A-Z]{2,}[\-]*[0-9]*[A-Z]*", communique_text_dict[key])
print(acronymes)




with open('acronymes.txt', 'w') as f:
    for key in acronymes.keys():
        f.write("%s,%s\n"%(key,str(acronymes[key])))

