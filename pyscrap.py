import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from csv import writer
import requests
import json
import re
import io
import os
def main():
    listurls = []
    dict1 ={}
    r = requests.get("https://webapps.muhlenberg.edu:442/Calendar/EventList.aspx?fromdate=08%2f01%2f2019&todate=05%2f31%2f2020&view=DateTime") #original page of the Event calender
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
        title1 = str(titleget)
        title = strip_non_ascii(title1)
        datesandtime = opp2.find_all('td', attrs={'s', 'detailsview'})
        resultsSD = datesandtime[2]
        resultsST = datesandtime[4]
        resultsED = datesandtime[6]
        resultsET = datesandtime[8]
        StartDate = str(resultsSD.contents[0])
        StartTime = str(resultsST.contents[0])
        try:
            EndDate = str(resultsED.contents[0])
        except IndexError:
            EndDate = "null"
        #print(count)
        try:
            EndTime = str(resultsET.contents[0])
        except IndexError:
            EndTime = "null"
        try:
            location = datesandtime[10]
            location1 = str(location.contents[1].get_text())
        except IndexError:
            location1 = "null"
        categories = opp2.find("span", attrs={'class', 'title'})
        #print(categories.contents)
        category = str(categories.contents[0])
        description = opp2.find_all('td', attrs={'class', 'detailsview'})
        #print(description[9].text)
        try:
            eventDescription1 = str(description[9].text[18:])
        except IndexError:
            eventDescription1 = "null"
        eventDescription = strip_non_ascii(eventDescription1)
        #eventDescription = stripbad(eventDescription2)
        dict1[count]={}
        dict1[count]["title"]=title
        dict1[count]["StartDate"]=StartDate 
        dict1[count]["StartTime"]=StartTime
        dict1[count]["EndDate"]=EndDate
        dict1[count]["EndTime"]=EndTime
        dict1[count]["Category"]=category
        dict1[count]["EventDesc"]=eventDescription
        dict1[count]["Location"] = location1
        
        
    remove =[]
    for key, items in dict1.items():
        if dict1[key].get('Category') == "Academic Calendar" or dict1[key].get('Category') == "Alumni" or dict1[key].get('Category') == "Common Hour" or dict1[key].get('Category') == "Community" or dict1[key].get('Category') == "Facility Hours" or dict1[key].get('Category') == "Information & Advisement" :
            remove.append(key)
    #print(remove)
    for i in remove:
        dict1.pop(i)
    #print(dict1)
    with io.open("the_file.json", "w", encoding="utf8") as f:
        json.dump(dict1, f)
         

    

    

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127 )
    return ''.join(stripped)
'''def stripbad(string):
    result = re.match(r"\r\n*", string)
    text = result.group(0)
    last = None
    output = []

    for c in text:
        if c == '.':
            output.append(c)
        elif c != last:
            if c in string.punctuation:
                last = c
            output.append(c)

         
    return ''.join(output)'''
main()