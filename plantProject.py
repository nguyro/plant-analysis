"""
Analyzing USDA plant Data
"""

from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# web scraping 
def create_browser():
    """
    chrome selenium object that mimics a browser
    """
    chrome_options = Options()
    # creates an invisible browser
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    print("Created Chrome Browser")
    return browser

url='https://plants.sc.egov.usda.gov/csvdownload?plantLst=plantCompleteList'
browser = create_browser() 
browser.get(url)
# wait 15 seconds for real page to load
time.sleep(15) 
page_html = browser.page_source
browser.quit()

# extracting data from downloaded html (alt to web scraping)
#with open("USDA Plants Database.htm", encoding="utf8") as usdaFile:
#        usdaSoup = soup(usdaFile, 'html.parser')

# parse html
usdaSoup = soup(page_html, 'html.parser')
usda = usdaSoup.pre.get_text().split('\n')

# splitting individual entry data
for i in range(len(usda)):
    usda[i] = re.split(r',(?=")', usda[i])
    for j in range(len(usda[i])):
        usda[i][j] = usda[i][j].replace('"','')


# creating dataframe and cleaning up data
df = pd.DataFrame(data=usda[1:])

# entry 92926 has 6 columns from incorrect data entry
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