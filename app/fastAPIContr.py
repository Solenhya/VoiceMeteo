import meteorequest
import voice
import dataParse
from fastapi import FastAPI , File , UploadFile
import tempfile

from json import JSONEncoder
import json
import numpy
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def ReplaceCode(code):
    if(code<=29):
        return("Pas de précipitation")
    elif(code<=35):
        return("Tempete de sable")
    elif(code<=39):
        return("Manteau de neige")
    elif(code<=49):
        return("Brouillard")
    elif(code<=59):
        return("Bruine")
    elif(code<=69):
        return("Pluie")
    elif(code<=79):
        return("Neige")
    elif(code<=86):
        return("Averse")
    elif(code<=90):
        return("Grêle")
    elif(code<=99):
        return("Tempete")
    else:
        return("Code inconnue")

app = FastAPI()

import NerTransform


def predictionSimple(info):
    difference = info["difference"]
    loc = info["loc"]
    retour = meteorequest.GetMeteoDailyDay(loc["latitude"],loc["longitude"],difference)
    return retour

def predictionAll(info):
    loc = info["loc"][0]
    print(f"Date = {info['date']}")
    min,max = dataParse.GetDateRange(info["date"])
    print(f"Min day = {min}")
    print(f"Max day = {max}")
    retour = meteorequest.GetMeteoDailyRange(loc["latitude"],loc["longitude"],min,max)
    return retour


@app.get("/")
def read_root(x=None):
    '''
    Essai de point d'API de base...

    :param x: première variable d'essai
    :return: un JSON standard
    '''
    return {"Hello": f"World, x={x}"}

@app.get("/meteo")
def getMeteo(longitude=0,latitude=0):
    retour = meteorequest.GetMeteoDailySimple(latitude,longitude)
    retour["weather_code"] = [ReplaceCode(x) for x in retour["weather_code"]]
    print(f"Type :: {type(retour['precipitation_probability_mean'][0])}")
    retour = json.dumps(retour,cls=NumpyArrayEncoder)
    return retour


@app.get("/voice")
def getVoice():
    retour = voice.recognize_from_microphone()
    #if retour pas bon
    return retour

@app.get("/nerInfo")
def getNer(text):
    ner = NerTransform.GetInfoAll(text)
    print(f"NER done : {ner}")
    retour = dataParse.parseAll(ner)
    if(retour["status"]!="Success"):
        pass
        #TODO pour monitoring
    return retour

#Une fonction pour creer la requete au service météo
#@app.post("/meteoFromNer") Erreur avec le transfert en requete du resultat du ner

def ExtractFirstMeteo(info):
    print(info)
    if(len(info["loc"])==0):
        print("Erreur localisation")
        return
        #TODO monitoring
    if(len(info["date"])==0):
        print("Erreur date")
        return
        #TODO monitoring
    #Choix du premier 
    loc = info["loc"][0]
    dates = info["date"][0]
    meteoReq = meteorequest.GetMeteoDay(loc["latitude"],loc["longitude"],[dates])
    if(len(meteoReq)==0):
        print("Meteo vide")
        return
        ##TODO cas ou les date n'était pas correct
    return meteoReq[0]

@app.get("/predictS")
def prediction(text):
    ner = NerTransform.GetInfoOne(text)
    print(f"Ner pour prediction fait : {ner}")
    info = dataParse.parseSingleData(ner)
    if(info==None):
        return "Erreur lors du traitements du text"
    prediction = predictionSimple(info)
    prediction["weather_code"] = [ReplaceCode(x) for x in prediction["weather_code"]]
    retour = prediction
    retour["date"]=[str(info["date"])]
    retour = json.dumps(retour,cls=NumpyArrayEncoder)
    return retour

@app.get("/predictA")
def PredictAll(text):
    ner = getNer(text)
    retour= ExtractFirstMeteo(ner)
    retour["weather_code"]=retour["weather_code"].apply(ReplaceCode)
    return retour.to_dict()
    try:
        ner = NerTransform.GetInfoAll(text)
    except:
        print("Erreur lors du Ner")
    finally:
        info = dataParse.parseAll(ner)
        if(info["status"]=="Success"):
            prediction=predictionAll(info)
            prediction["weather_code"] = [ReplaceCode(x) for x in prediction["weather_code"]]
            retour = prediction
            #retour["date"]=[str(info["date"])]
            retour = retour.to_dict(orient="list")
            retour = json.dumps(retour,cls=NumpyArrayEncoder)
            return retour
        else:
            print("Erreur lors du parsing")

#Essai fonction fastAPi qui a besoin de react
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # Save the file temporarily
    file_path = f"temp_audio.wav"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    transcript = voice.recognize_from_file("temp_audio.wav")

    return {"transcription": transcript}