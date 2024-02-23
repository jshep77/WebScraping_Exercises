import json
import os
from urllib.request import urlopen, urljoin
import requests
import re
import webbrowser


def FileTypeID(filename):
    file_type = filename.split(".")
    file_extention = file_type[1]
    return "The file format is:"+ file_extention.upper()

#print(FileTypeID("testing.py"))



class Read_Data:
    def __init__(self):
        pass

    def Get_Num_Lines(self):
        self.numlines = input("Please enter the number of lines you wish to have printed:")
    
    def Print_Lines(self,file):
        str_file = os.path.splitext(file)[0]
        txt_file = str(str_file+'.txt')
        numlines = int(self.numlines)
        count = 0
        with open(file, 'r') as f, open(txt_file,'w') as txt:
            data = json.load(f)
            indata = json.dumps(data,indent=2)
            txt.write(indata)
        with open(txt_file,'r') as new:
            while True:
                count += 1
                line = new.readline()
                if (count>numlines):
                    break
                print(line)

#reader = Read_Data()
#reader.Get_Num_Lines()
#reader.Print_Lines("Assignment2\Electric_Vehicle_Population_Data.json")


def FileConverter(file):
    filename1 = os.path.splitext(file)[0] + '_toHTML'
    htmlfile = str(filename1+'.html')
    filename2 = os.path.splitext(file)[0] + '_toCSV'
    csvfile = str(filename2+'.csv')
    print(filename1, filename2)
    with open(file, 'r') as original, open(filename1,'w') as html, open(filename2,'w') as csv:
        data = original.read()
        html.write(data)
        csv.write(data)
    os.rename("Assignment2\Electric_Vehicle_Population_Data_toHTML",htmlfile)
    os.rename("Assignment2\Electric_Vehicle_Population_Data_toCSV",csvfile)

#FileConverter("Assignment2\Electric_Vehicle_Population_Data.json")



def last_10_lines():
    jsonfile = str('Assignment2/sample.json')
    html_response = requests.get(url= "https://en.wikipedia.org/wiki/Data_science")

    with open("Assignment2/sample.html", "a", encoding="utf-8") as html_file:
        html_file.write(html_response.text)
    os.rename("Assignment2/sample.html",jsonfile)
    with open("Assignment2/sample.json", "r", encoding="utf-8") as json1:
        lines = json1.readlines()
        last_10_lines = lines[-10:]
        for line in last_10_lines:
            print(line)

#last_10_lines()



def URLimageExtract():
    url = "https://en.wikipedia.org/wiki/Twitter"
    webpage = urlopen(url).read().decode('utf-8')
    imagetag = re.compile('<img[^>]+src=["\'](.*?)["\']',re.IGNORECASE)
    image_links = imagetag.findall(webpage)
    for src in image_links:
        print(urljoin(url,src))
    listlen = len(image_links)
    lastlink = urljoin(url,image_links[listlen-1])
    webbrowser.open(lastlink)

#URLimageExtract()




def yearExtract():
    url = "https://en.wikipedia.org/wiki/Twitter"
    webpage = urlopen(url).read().decode('utf-8')
    years = re.compile('\s(?:19|20)\d{2}\D')
    all_years = years.findall(webpage)
    result = [substring[:-1] for substring in all_years]
    print(result)

#yearExtract()


def pandemicSentences():
    webpage = urlopen("https://en.wikipedia.org/wiki/Twitter").read().decode('utf-8')
    pattern = re.compile("[A-Z][^.!?]*pandemic[^.!?]*[.!?]")
    sentences = re.findall(pattern, webpage)
    with open("Assignment2/pandemic_sent_file.json",'a') as file:
        for sentence in sentences:
            file.write(sentence)
            file.write("\n")

pandemicSentences()        


def extractPostCode():
    url = " https://www.indiana.edu/"
    webpage = urlopen(url).read().decode('utf-8')
    postcode = re.compile("\d{5}-\d{4}")
    postal_codes = re.findall(postcode, webpage)
    print(postal_codes)

#extractPostCode()