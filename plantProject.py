# -*- coding: utf-8 -*-
"""
plants
"""
from bs4 import BeautifulSoup as soup
#import requests
import re
import pandas as pd
import numpy as np

# web scraping 
#url='https://plants.sc.egov.usda.gov/csvdownload?plantLst=plantCompleteList'
#html_text = requests.get(url).text
#p = soup(html_text.content, 'html.parser')

with open("USDA Plants Database.html", encoding="utf8") as usdaFile:
        usdaSoup = soup(usdaFile, 'html.parser')

usda = usdaSoup.pre.get_text().split('\n')

# splitting individual entry data
for i in range(len(usda)):
    usda[i] = re.split(r',(?=")', usda[i])
    for j in range(len(usda[i])):
        usda[i][j] = usda[i][j].replace('"','')


## creating dataframe and cleaning up data
df = pd.DataFrame(data=usda[1:])

# entry 92926 has 6 columns from incorrect data entry, drop empty column
df = df.drop(columns=5)

# add variable names
usdaCol = usda[0]
df.columns = usdaCol

# seperating scientific name from author name
' '.join(df['Scientific Name with Author'][2].split(' ',2)[:2])
df['Scientific Name'] = df['Scientific Name with Author'].apply(
    lambda x: ' '.join(x.split(' ',2)[:2]))
df['Author'] = df['Scientific Name with Author'].apply(
    lambda x: ' '.join(x.split(' ',2)[2:]))
df = df.drop(columns = 'Scientific Name with Author')

# capitalizing common name
df['Common Name'] = df['Common Name'].apply(lambda x: x.title())

# replacing blanks with nan
df.replace('', np.nan, regex=True, inplace = True)