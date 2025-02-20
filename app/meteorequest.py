import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def getMeteoDataDaily(latitude,longitude,dailyReq,days=4):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    "latitude": latitude,
	"longitude": longitude,
    "daily":",".join(dailyReq),
    "forecast_days":days
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    daily = response.Daily()
    
    #retour = {"date": pd.date_range(
	#start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	#end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	#freq = pd.Timedelta(seconds=daily.Interval()),
	#inclusive = "left"
    #)}
    retour = {}
    for i in range(len(dailyReq)):
        colName = dailyReq[i]
        retour[colName]=daily.Variables(i).ValuesAsNumpy()
    return retour

def GetMeteoDailyRange(longitude,latitude,dailyReq,minRange,maxRange):
    data = getMeteoDataDaily(longitude,latitude,dailyReq,days=maxRange)
    return data[minRange:]




# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 47.3948,
	"longitude": 0.704,
	"hourly": "temperature_2m,cloud_cover,precipitation_probability",
    "forecast_days":16,
    "daily":"precipitation_probability_mean"
}

listeDaily = ["precipitation_probability_mean","temperature_2m_min","temperature_2m_max","weather_code"]

#meteo = getMeteoDataDaily(0,47,listeDaily)

#print(meteo)


def GetMeteoDailySimple(latitude,longitude):
    return getMeteoDataDaily(latitude,longitude,listeDaily)