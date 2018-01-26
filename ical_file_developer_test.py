import urllib.request
from icalendar import Calendar
from datetime import datetime
import unittest

"""
Program to display bin collection details
Porgram takes input in format Y-m-d
Returns schedule of next bin collection

"""

def test_closest_date():
    assert getClosestDate([datetime.strptime("2018-01-16", "%Y-%m-%d").date(), datetime.strptime("2018-02-13", "%Y-%m-%d").date()], datetime.strptime("2018-01-01", "%Y-%m-%d").date()) == datetime.strptime("2018-01-16", "%Y-%m-%d").date()

""" downloads remote ical to local machine"""        
def downloadFile(url,file_name):
    remote_file=urllib.request.urlopen(url)
    local_file = open(file_name,"wb")
    local_file.write(remote_file.read())
    local_file.close();

"""" sort the dates and search for the closest match"""
def extractAndSortDates(file_name, user_date):
    date_list=[]
    local_file = open(file_name,"rb")    
    ical_file = Calendar.from_ical(local_file.read())
    for component in ical_file.walk():
        if component.name == "VEVENT":        
            date_list.append(component.get('DTSTART').dt)

    date_list.sort()
    closest_date = getClosestDate(date_list, user_date)
    for component in ical_file.walk():
        if component.name == "VEVENT":
            if(component.get('DTSTART').dt == closest_date):
                print(component.get("SUMMARY"))
                print(component.get("DTSTART").dt)
    
    local_file.close();


def getClosestDate(date_list,user_date):
    nearest =[];
    for date in date_list:
        if date > user_date:
            nearest.append(date)           
    
    return nearest[0]

""""validate date format"""
def validateDate(user_date):
    try:
        datetime.strptime(user_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


user_date = input("Enter Date in Y-m-d format:  ")
validateDate(user_date)
user_date= datetime.strptime(user_date, "%Y-%m-%d").date()

url = "https://s3-eu-west-1.amazonaws.com/fs-downloads/GM/binfeed.ical"
file_name="ical_file.txt"

downloadFile(url, file_name)
extractAndSortDates(file_name, user_date)

test_closest_date()
