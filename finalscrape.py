import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from csv import writer
import requests
import json
import re
import io
import os
import string
def main():
    listurls = []
    dict1 ={}
    r = requests.get("https://webapps.muhlenberg.edu:442/Calendar/EventList.aspx?fromdate=08%2f01%2f2019&todate=05%2f31%2f2020&view=DateTime") #original page of the Event calender
    #print(r.text[0:500])
    opp = soup(r.text, "html.parser")
    results = opp.find_all('a', attrs={"class" : "url"}) #grabbing all the event urls
    for result in results:
        link = "https://webapps.muhlenberg.edu:442/Calendar/" + result.get('href') 
        #the urls did not include the first part of the URL so add it each time and created string
        listurls.append(link)

    
    count = 0
    for x in listurls: #loop through list of urls find the information that is wanted
        count+=1
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
        #print(title)
        try:
            EndDate = str(resultsED.contents[0])
        except IndexError:
            EndDate = "n/a"
        try:
            location = datesandtime[10]
            location1 = str(location.contents[1].get_text())
        except IndexError:
            location1 = "n/a"
        try:
            EndTime = str(resultsET.contents[0])
        except IndexError:
            EndTime = "n/a"
        #print(StartDate)
        #print(EndDate)
        categories = opp2.find("span", attrs={'class', 'title'})
        #print(categories.contents)
        category = str(categories.contents[0])
        description = opp2.find_all('td', attrs={'class', 'detailsview'})
        #print(description[9].text)
        try:
            eventDescription1 = str(description[9].text[18:])
        except IndexError:
            eventDescription1 = "n/a"
        location1 = location_match(location1)
        if("2019" in StartDate):
            year = "2019"
        if("2020" in StartDate):
            year = "2020"

        month = "0" + StartDate[0:2]
        if("/" in month):
            month = month.replace("/", "")
        if(len(month) > 2):
            month = month[1:]
        day = StartDate[2:4]
        if("/" in day):
            day = day.replace("/", "")
        #print(day)
        if( len(day) > 2):
            day = day[0] + "0" + day[1]
        if(len(day) == 1):
            day = "0" + day
        
        #year = StartDate[6:10]
        new_thang = year + "-" + month + "-" + day
        eventDescription = strip_non_ascii(eventDescription1)
        dict1[count]={}
        dict1[count]["title"]=title
        dict1[count]["StartDate"]=new_thang
        dict1[count]["StartTime"]=StartTime
        dict1[count]["EndDate"]=EndDate
        dict1[count]["EndTime"]=EndTime
        dict1[count]["Category"]=category
        dict1[count]["EventDesc"]=eventDescription
        dict1[count]["Location"] = location1

    #print(dict1)
    '''remove =[]
    for key, items in dict1.items():
        if dict1[key].get('Category') == "Academic Calendar" or dict1[key].get('Category') == "Alumni" or dict1[key].get('Category') == "Common Hour" or dict1[key].get('Category') == "Community" or dict1[key].get('Category') == "Facility Hours" or dict1[key].get('Category') == "Information & Advisement" :
            remove.append(key)
    for i in remove:
        dict1.pop(i)'''
    with io.open("format.json", "w", encoding="utf8") as outputfile:
        json.dump(dict1,outputfile, indent=4)

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127 )
    return ''.join(stripped)
def stripbad(string):
    result = re.match(r"\r\n*", string)
    return result.group(0)
def location_match(string):
    if("Seegers" in string):
        return "Seegers"
    if("Trumbower" in string):
        return "Trumbower"
    if("Shankweiler" in string):
        return "Shankweiler"
    if("Ettinger" in string):
        return "Ettinger"
    if("Moyer" in string):
        return "Moyer"
    if("" == string):
        return "Muhlenberg College"
    if("Chapel" in string):
        return "Chapel"
    if("Life Sports Center" in string):
        return "Life Sports Center"
    if("Center for the Arts" in string):
        return "Center for the Arts"
    else:
        return string
main()
