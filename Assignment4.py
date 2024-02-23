from docx2pdf import convert
import os
from bs4 import BeautifulSoup
import re

html_file = os.getcwd() + '\\Assignment4\\NOPAGETAB_NFHLWMS.html'
with open(html_file) as html:
    soup = BeautifulSoup(html, "lxml")

#2
filepath = os.getcwd() + "\\Assignment4\\UTT-Books.docx"
convert(filepath)

#3A number of word hazard
hazard_regex = r'\bhazard\b'
word_matches = re.findall(hazard_regex,soup.text,re.IGNORECASE)
print("Count of the word hazard: ",len(word_matches))

#3B extract the time of the file
time_regex = re.compile("\b\d:\d\b")
timestamptext = soup.find('p',class_="note").text
timestamp = timestamptext.split(":")[1:]
timestamp = ":".join(timestamp)
print("Time of last file update:", timestamp)

#3C extract all URL addresses
print("The following list is all of the links in the given document:")
http_regex = re.compile(r"(https?://\S+)")
for link in soup.find_all('a', href=http_regex):
    print(link.get('href'),"\n")