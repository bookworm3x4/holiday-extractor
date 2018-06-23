# holidayExtractor.py
# Emmett Wald
# 23 June 2018

# using html from http://interfaith-calendar.org/, creates nested dictionaries
# of year, month, day, and holiday info, then exports these dictionaries as
# csv files


################################################################################

# SAMPLE HTML
'''
ETCETERA
<h2 align="left">SEPTEMBER&nbsp; 2018</h2>

<ul>
<li>1 <ul>
	<li>Religious year begins - <b>Orthodox Christian </b> </li>
	</ul>
	</li>
<li>3 <ul>
	<li>Krishna Janmashtami ** - <b>Hindu</b></li>
	</ul>
	</li>
ETCETERA
'''

# SAMPLE DICTIONARY
'''
holidays = {2018: {'Sep': {1: ["Religious year begins", "Catholic Christian"],
                           3: ["Krishna Janmashtami", "Hindu"],
                           ETCETERA},
                   'Oct': {},
                   'Nov': {},
                   'Dec': {},
                   },
            2019: {}
            }
'''

# SAMPLE CSV
'''
year, month, day, holiday,               faith
2018, Sep,   1,   Religious year begins, Catholic Christian
2018, Sep,   3,   Krishna Janmashtami,   Hindu
ETCETERA
'''


################################################################################

years = [2018, 2019]

months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

fall = months[8:]

spring = months[:8]


################################################################################

# import html text from py file
from yrText import *


def main():    
    yr2018fall = trimFall()
    yr2019spring = trimSpring()

    #holidays = createDictionary()
    holidays = {}
    holidays[2018] = extract(fall, 2018, yr2018)
    holidays[2019] = extract(spring, 2019, yr2019)
    
    print(holidays)

    
def createDictionary():
    # create empty holidays dictionary
    holidays = {}
    
    # create empty year dictionaries w/in holidays
    for yr in years:
        holidays[yr] = {}

    # create empty month dictionaries w/in years
    for month in fall:
        holidays[years[0]][mon] = {}
    for month in spring:
        holidays[years[1]][mon] = {}

    return holidays


def trimFall():
    # find september, remove everything before it
    locSep = yr2018.find("SEPTEMBER")
    yr2018fall = yr2018[locSep:]

    return yr2018fall


def trimSpring():
    # find january, remove everything before it
    locJan = yr2019.find("JANUARY")
    locSep = yr2019.find("SEPTEMBER")
    yr2019spring = yr2019[locJan:locSep]

    return yr2019spring


def extract(semester, year, yrHTML):
    # initialize dictionary for the semester
    semesterDict = {}

    # loop through each month in the semester
    for month in semester:

        # create empty dictionary for the month
        semesterDict[month] = {}
        
        # create a variable to hold the html for that month only
        nextMonth = semester[semester.index(month) + 1]
        loc0 = yrHTML.find(month.upper())
        loc1 = yrHTML.find(nextMonth.upper())
        monthData = yrHTML[loc0:loc1]

        # loop through days in the month
        while True:

            # find the html tag that starts a day listing
            dayLoc0 = monthData.find("<li>") + 4

            # if you can't find one, the month is done
            if dayLoc0 == -3:
                break
            
            # remove stuff prior to start of day
            monthData = monthData[dayLoc0:]
            # find the html tag for the first item after the day number(s)
            dayLoc1 = monthData.find("<ul>")
            # create a variable to hold the day number(s)
            day = monthData[:dayLoc1].strip()
            # create an empty list for the day(s)
            semesterDict[month][day] = []

            # find the tag that marks the end of a day listing
            dayEndLoc = monthData.find("</ul>")
            # create a marker for where in the day we are
            current = 0
            while True:
                # remove everything prior to current location
                shortMonthData = monthData[current:dayEndLoc]
                
                # find the html tag that marks a holiday listing
                holLoc0 = shortMonthData.find("<li>") + 4
                # if we can't find one, the day is done
                if holLoc0 == -3:
                    break
                
                # find the other html tags for the holiday listing
                holLoc1 = shortMonthData.find(" - <b>")
                holLoc2 = holLoc1 + 6
                holLoc3 = shortMonthData.find("</b>")
                # add holiday info to list
                holName = shortMonthData[holLoc0:holLoc1]
                faith   = shortMonthData[holLoc2:holLoc3]
                semesterDict[month][day].append([holName, faith])
                # update marker for current location
                current = holLoc3

            # find the end of the day, remove the day
            dayEndLoc = monthData[dayEndLoc:].find("</li>")
            monthData = monthData[dayEndLoc:]

    return semesterDict


main()
