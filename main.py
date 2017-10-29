import requests
import time
import calendar
import numpy as np

headers = {
    "token": 'tTdIaBDSeBHYQSVbchOedDgsQZTsIzIj'
}

datatypeid = 'TMAX'
locationid = 'FIPS:25017'
startdate = '2017-01-01'
enddate = '2017-01-02'

url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'

url += "?datasetid=GHCND"
url += '&datatypeid=' + datatypeid
url += '&locationid=' + locationid
url += '&units=standard'

standard_url = url

url += '&startdate=' + startdate
url += '&enddate=' + enddate
url += '&limit=1'

# pull first station in the county
response = requests.get(url, headers=headers)
response = response.json()
stationid = response['results'][0]['station']

print("station is " + stationid)


# month is an int
# e.g. january is 1
def getTempForMonth(stationid, month):
    days = calendar.monthrange(2017, month)[1]
    temps = []

    mm = str(month)
    if len(mm) == 1:
        mm = "0" + mm

    for day in range(1, days):
        dd = str(day)
        if len(dd) == 1:
            dd = "0" + dd

        mmdd = mm + "-" + dd

        temp = getTempForDay(stationid, 2010, 2017, mmdd)
        print("{} temp on {}-{}".format(temp, mm, dd))
        temps.append(temp)

    return temps


# mmdd is a string of the month and day you want to check
# e.g. january first is '01-05'
def getTempForDay(stationid, startyear, endyear, mmdd):
    total = 0
    missing = 0
    for i in range(startyear, endyear):
        year = str(i)
        date = year + "-" + mmdd
        temp = getTemp(stationid, date)
        if temp == -504:
            missing += 1
        else:
            total += temp
        time.sleep(0.21)  # max of 5 requests a second

    return total / (endyear - startyear - missing)


def getTemp(stationid, start):
    url = standard_url
    url += "&stationid=" + stationid
    url += '&startdate=' + start
    url += '&enddate=' + start
    url += '&limit=1'

    response = requests.get(url, headers=headers)
    response = response.json()
    if len(response) > 0:
        return response['results'][0]['value']
    else:  # no data
        return -504


# A UsefulTemps10 is a Dict
# Keys are temperatures in ten-degree increments
# Values are how many temperatures are 10 degrees or less greater
# example_usefultemps = {"-10":2,"0":3,"10":4}
# represents
# two temps between [-10,0)
# three temps between [0,10)
# four temps between [10,20)

# Takes in an array of temperatures and returns them in a more useful format
# Array -> UsefulTemps10
def parse(data):
    a = np.array(data)
    out = {}
    for temp in range(-10, 100, 10):
        matches = len(a[(a >= temp) & (a < (temp + 10))])
        if matches > 0:
            out[str(temp) + "-" + str(temp+10)] = matches

    return out


print(parse(getTempForMonth(stationid, 1)))
