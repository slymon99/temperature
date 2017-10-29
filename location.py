import requests

headers = {
    "token": 'tTdIaBDSeBHYQSVbchOedDgsQZTsIzIj'
}

def stations(locationid):
    datatypeid = 'TMAX'
    startdate = '2017-01-01'
    enddate = '2017-01-02'

    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
    url += "?datasetid=GHCND"
    url += '&datatypeid=' + datatypeid
    url += '&locationid=' + locationid
    url += '&startdate=' + startdate
    url += '&enddate=' + enddate

    response = requests.get(url, headers=headers)
    response = response.json()

    results = []
    for entry in (response['results']):
        results.append(entry['station'])

    return results

print(stations('FIPS:25017'))