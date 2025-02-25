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
    
    #Creer un datetimeindex correspondant a l'intervalle entre le début et la fin de la prédiction
    retour = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds=daily.Interval()),
	#inclusive = "left"
    )}

    #Extrait les jours et les mois 
    retour["days"]=retour["date"].day.tolist()
    retour["months"]=retour["date"].month.to_list()
    
    #Coupe si on a un jour en trop
    retour["days"]=retour["days"][:16]
    retour["months"]=retour["months"][:16]

    retour.pop("date",None)

    #Rajoute dans le dictionnaire toute les variables selecionner
    for i in range(len(dailyReq)):
        colName = dailyReq[i]
        retour[colName]=daily.Variables(i).ValuesAsNumpy()
    return retour



listeDaily = ["precipitation_probability_mean","temperature_2m_min","temperature_2m_max","weather_code"]
maxdays = 16
def GetMeteoInfo(latitude,longitude):
    data = getMeteoDataDaily(latitude,longitude,listeDaily,days=maxdays)
    return data

#Prend une latitude,longitude et une liste de date formater et renvoi une liste de dataframe qui correspondents
def GetMeteoDay(latitude,longitude,days):
    data = GetMeteoInfo(latitude,longitude)
    data = pd.DataFrame(data)
    retour = []

    #TODO gerer le cas la date est dans le passé ou trop loin dans le futur ( faire un retour special)
    for dateF in days:
        df_filtered = data[data.apply(lambda row: dateF.Correspond(row['days'], row['months']), axis=1)]
        retour.append(df_filtered)
    return retour

    