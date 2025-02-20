import meteorequest
import voice
from fastapi import FastAPI

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



print("Création model Ner")
from transformers import CamembertTokenizer, AutoModelForTokenClassification
from transformers import pipeline
tokenizer = CamembertTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
NerPipeline = pipeline("ner",model=model,tokenizer=tokenizer,aggregation_strategy="simple")
print("Modele charger")


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
    retour = json.dumps(retour,cls=NumpyArrayEncoder)
    return retour


@app.get("/voice")
def getVoice():
    return voice.recognize_from_microphone()

@app.get("/ner")
def getNer(text):
    retour = NerPipeline(text)
    retour = json.dumps(retour,cls=NumpyArrayEncoder)
    return retour