import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from csv import writer
import requests
import json
import re
import io
listurls = []
dict1 ={}
r = requests.get("https://webapps.muhlenberg.edu:442/Calendar/") #original page of the Event calender
#print(r.text[0:500])
opp = soup(r.text, "html.parser")
results = opp.find_all('a', attrs={"class" : "url"}) #grabbing all the event urls
for result in results:
    link = "https://webapps.muhlenberg.edu:442/Calendar/" + result.get('href') #the urls did not include the first part so add it each time and create string
    listurls.append(link)

#print(listurls)
#file1 = open("urls.txt", "w")
count = 0
for x in listurls: #loop through list of urls find the information that is wanted
    count+=1
    #file1.write(x)
    #file1.write('\n')
#file1.close()
#with open("urls.txt", "r") as fp:
    #line = fp.readline()
    x2 = requests.get(x)
    opp2 = soup(x2.text, "html.parser")
    titleget = opp2.find('td', attrs={'class', 'listheadtext'}).text
    title = str(titleget)
    datesandtime = opp2.find_all('td', attrs={'s', 'detailsview'})
    resultsSD = datesandtime[2]
    resultsST = datesandtime[4]
    resultsED = datesandtime[6]
    resultsET = datesandtime[8]
    StartDate = str(resultsSD.contents[0])
    StartTime = str(resultsST.contents[0])
    EndDate = str(resultsED.contents[0])
    #print(count)
    try:
        EndTime = str(resultsET.contents[0])
    except IndexError:
        EndTime = "null"
    categories = opp2.find("span", attrs={'class', 'title'})
    #print(categories.contents)
    category = str(categories.contents[0])
    description = opp2.find_all('td', attrs={'class', 'detailsview'})
    #print(description[9].text)
    eventDescription = str(description[9].text[18:])
    dict1[title]={}
    dict1[title]["StartDate"]=StartDate 
    dict1[title]["StartTime"]=StartTime
    dict1[title]["EndDate"]=EndDate
    dict1[title]["EndTime"]=EndTime
    dict1[title]["Category"]=category
    dict1[title]["EventDesc"]=eventDescription

#print(dict1)
with open ("format.json", "w", encoding="utf8") as outputfile:
    json.dump(dict1,outputfile, indent=4)

