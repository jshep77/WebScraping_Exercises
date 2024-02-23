import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
import pandas as pd
import time
from selenium.webdriver.common.by import By
import re
import webbrowser
import tweepy
from datetime import datetime

consumer_key = "tX6x8Kz0ntLLTEB6P2y5b64nB"
consumer_secret = "ppgkCA7OR8DKjUwE7yTfy7oCwDSHa80WsdgDHhaohPwN0SonXJ"
access_token = "1457374016277303297-dNg6ino7PdGr90uHK0lxfXXpzgFq5l"
access_token_secret = "j9a4mXWXifdR5m7DSrXXdaXFD2V6tT3HCIFVprzHcR9PT"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
tag = "#happy"
tweets = tweepy.Cursor(api.search_tweets, q=tag).items(1000)
Twitter_ID, Language, Screen_Name, Text  = [], [], [], []
for tweet in tweets:
    Twitter_ID.append(tweet.user.id_str)
    Language.append(tweet.lang)
    Screen_Name.append(tweet.user.screen_name)
    Text.append(tweet.text)
data = pd.DataFrame({"ID" : Twitter_ID, "Language" : Language, "Screen Name" : Screen_Name, "Text" : Text})
data.to_csv("tweets.csv", columns=["ID","Language","Screen Name","Text"], index=False)
#A
driver.get("https://archive.ics.uci.edu/datasets")
#B
allpagetext = driver.find_element(By.XPATH, "/html").text
print(allpagetext)

#C
nextpagebutton = driver.find_element(By.XPATH, '//button[@aria-label="Next Page"]')
pattern = re.compile(r'\bregression\b', re.IGNORECASE)
countlist = []
pagecount = 0
while pagecount < 11:
    for element in allpagetext:
        match = pattern.match(element)
        if match:
            countlist.append(element)
    if (len(countlist) > 0):
        print("Count of Regression", len(countlist))
        break
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    nextpagebutton.click()
    pagecount += 1
    allpagetext = driver.find_element(By.XPATH, "/html").text
if(len(countlist)==0):
    print("Regression doesn't appear on the first ten pages")

#D
col1 = []
col2 = []
col3 = []
col4 = []

DataSetNames = driver.find_elements(By.XPATH, '//div[@role="row"]//h2[@class="truncate text-primary"]')
DataTypes = driver.find_elements(By.XPATH, '//div[2]/div/div[2]/span')
DefaultTaskAttribute = driver.find_elements(By.XPATH, '//div[1]/div[2]/div/div[1]/span')
elements = driver.find_elements(By.XPATH, '//div[@class="my-2 hidden gap-4 md:grid grid-cols-12"]//following-sibling::*[local-name()="svg"]')
for element in elements:
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(.5)
    element.click()
Year = driver.find_elements(By.XPATH, '//tr/td[3]')

for dataname in DataSetNames:
    col1.append(dataname.text)
for datatype in DataTypes:
    col2.append(datatype.text)
for attribute in DefaultTaskAttribute:
    col3.append(attribute.text)
for year in Year:
    col4.append(year.text)

listofAll = [col1, col2, col3, col4]
data = pd.DataFrame(listofAll).T
data.columns = ["DataSetNames","DataTypes","DefaultTaskAttribute","Year"]
pd.to_datetime(data.Year, format='%m/%d/%Y',errors='ignore')
split = data['Year'].str.split('/', expand=True)
data['Years'] = split[2]
data['Months'] = split[0]
data = data.sort_values(by=['Years','Months'], ascending=[False,False])
data.to_csv("extract.csv", index=False, columns=["DataSetNames","DataTypes","DefaultTaskAttribute","Year"])

#4
webbrowser.open("https://www.indeed.com")