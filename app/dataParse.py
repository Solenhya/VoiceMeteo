import dateparser
import requests
import datetime

def parseSingleData(info):
    date = info["date"]
    date = dateparser.parse(date,settings={'PREFER_DATES_FROM': 'future'})
    info["date"]=date
    print(f"Date parsed : {date}")
    difference = date-datetime.datetime.now()
    info["difference"]=difference.days+1
    loc = info["loc"]
    requete = requests.get("https://api-adresse.data.gouv.fr/search/",params={"q":loc})
    cord = requete.json()["features"][0]["geometry"]["coordinates"]
    long = cord[0]
    lat=cord[1]
    print(f"Loc parsed :\nlattitude - {lat}\nlongitude - {long}")
    info["loc"]={"latitude":lat,"longitude":long}
    return info