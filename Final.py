import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

US_Banks=[]
American_Banks=[]
International_Banks=[]

URL = "https://www.reddit.com/search/?q=us+banks"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'lxml')

URL1 = "https://www.reddit.com/search/?q=american+banks"
r1 = requests.get(URL1)
soup1 = BeautifulSoup(r1.content, 'lxml')

URL2 = "https://www.reddit.com/search/?q=international+banks"
r2 = requests.get(URL2)
soup2 = BeautifulSoup(r2.content, 'lxml')

table = soup.find_all('a', attrs={'data-testid' : 'post-title'})
for row in table:
	item = []
	item = row.text
	US_Banks.append(item)
	
table = soup1.find_all('a', attrs={'data-testid' : 'post-title'})
for row in table:
	item = []
	item = row.text
	American_Banks.append(item)
	
table = soup2.find_all('a', attrs={'data-testid' : 'post-title'})
for row in table:
	item = []
	item = row.text
	International_Banks.append(item)

if (len(US_Banks) < len(American_Banks) & len(International_Banks)):
	American_Banks = American_Banks[:len(US_Banks)]
	International_Banks = International_Banks[:len(US_Banks)]
elif (len(American_Banks) < len(US_Banks) & len(International_Banks)):
	US_Banks = US_Banks[:len(American_Banks)]
	International_Banks = International_Banks[:len(American_Banks)]
elif (len(International_Banks) < len(American_Banks) & len(US_Banks)):
	American_Banks = American_Banks[:len(International_Banks)]
	US_Banks = US_Banks[:len(International_Banks)]

data = pd.DataFrame({"US Banks": US_Banks, "American Banks": American_Banks, "International Banks": International_Banks})
data = data.replace(r'\n','', regex=True)
data = data.replace(r',','', regex=True)
data = data.replace(r'[^\w\s]+','', regex=True)
data['US Banks'] = data['US Banks'].str.lower()
data['American Banks'] = data['American Banks'].str.lower()
data['International Banks'] = data['International Banks'].str.lower()
datacount1 = data['US Banks'].str.split().explode().value_counts()
datacount2 = data['American Banks'].str.split().explode().value_counts()
datacount3 = data['International Banks'].str.split().explode().value_counts()
datacount = pd.DataFrame({"US Banks": datacount1, "American Banks": datacount2, "International Banks": datacount3})
datacount = datacount.fillna(0)
datacount['Sum'] = datacount.sum(axis=1)
datacount = datacount.sort_values(by='Sum', ascending=False)
datacount.to_csv("Mini Project/mini_project_datacount.csv")
data.to_csv("Mini Project/mini_project_data.csv",columns=["US Banks","American Banks","International Banks"])

top20words = datacount.head(20)
top20words.plot(kind='bar')
plt.show()

filteredtop20 = datacount.drop(['banks', 'you', 'all', 'do', 'if', 'or', 'how', 'their', 'its', 'be', 'out', 'of','for','in', 'to', 'the', 'are', 'and', 'a', 'on', 'is', 'from' 'as', 'with', 'by', 'as', 'was', 'it', 'that', 'have', 'us', 'american', 'international', 'see', 'we', 'need'], errors='ignore')
filteredtop20 = filteredtop20.head(20)
filteredtop20.plot(kind='bar')
plt.show()

USBANKtext = " ".join(data['US Banks'])
wordcloud = WordCloud().generate(USBANKtext)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

AMERICANtext = " ".join(data['American Banks'])
wordcloud = WordCloud().generate(AMERICANtext)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

INTERNATIONALtext = " ".join(data['International Banks'])
wordcloud = WordCloud().generate(INTERNATIONALtext)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()