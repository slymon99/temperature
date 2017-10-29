import requests

headers = {
    "token":'tTdIaBDSeBHYQSVbchOedDgsQZTsIzIj'
}
url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&locationid=FIPS:25017&units=standard&stationid=GHCND:USC00194313&startdate=1970-07-30&enddate=1970-07-30&limit=1'
response = requests.get(url, headers = headers)
response = response.json()
print len(response)