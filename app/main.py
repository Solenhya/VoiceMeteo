import services.meteorequest as meteorequest
import services.voice as voice
import services.dataParse as dataParse
import services.NerTransform as NerTransform
from fastapi import FastAPI , File , UploadFile , Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
from pydantic import BaseModel

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
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/test")
def read_root(x=None):
    '''
    Essai de point d'API de base...

    :param x: première variable d'essai
    :return: un JSON standard
    '''
    return {"Hello": f"World, x={x}"}

@app.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    return templates.TemplateResponse(
        request=request, name="accueilVoc.html"
    )

def formatMeteo(meteo):
    meteoSel=meteo[0]
    meteoSel["weather_code"]=meteoSel["weather_code"].apply(ReplaceCode)
    meteoSel["days"] = meteoSel["days"].astype(str) + "/" + meteoSel["months"].astype(str)
    meteoSel.drop(["months"],axis=1,inplace=True)
    meteoSel["temperature_2m_max"]=meteoSel["temperature_2m_max"].apply(lambda x: round(x, 2))
    meteoSel["temperature_2m_min"]=meteoSel["temperature_2m_min"].apply(lambda x: round(x, 2))
    meteoSel.rename(columns={"days":"date","precipitation_probability_mean":"Probailité de précipitation","temperature_2m_min":"Temperature Minimum","temperature_2m_max":"Temperature Maximum","weather_code":"Code Météo"},inplace=True)
    rowdict = meteoSel.iloc[0].to_dict()
    return rowdict

@app.get("/meteo2",response_class=HTMLResponse)
def getMeteo2(request: Request,day:int,month:int,latitude:float,longitude:float):
    print(f"Date : {day}/{month}")
    print(f"Loc : {latitude},{longitude}")
    date = dataParse.DateFormatCust({"day":day,"month":month})
    meteo = meteorequest.GetMeteoDay(latitude,longitude,[date])
    print(meteo[0])
    print(meteo[0].to_dict())
    rowdict = formatMeteo(meteo)
    return templates.TemplateResponse(
        request=request, name="resultMeteo.html" , context={"meteo":rowdict}
    )
@app.get("/meteo",response_class=HTMLResponse)
def getMeteo(request: Request,day:int,month:int,localisation):
    print(f"Date : {day}/{month}")
    print(f"Loc : {localisation}")
    date = dataParse.DateFormatCust({"day":day,"month":month})
    loc = dataParse.getLL(localisation)
    meteo = meteorequest.GetMeteoDay(loc["latitude"],loc["longitude"],[date])
    print(meteo[0])
    print(meteo[0].to_dict())
    rowdict = formatMeteo(meteo)
    return templates.TemplateResponse(
        request=request, name="resultMeteo.html" , context={"meteo":rowdict,"localisation":localisation}
    )
class RequestModel(BaseModel):
    text: str

@app.post("/nerInfo")
def getNer(request: RequestModel):
    text = request.text
    print(f"Ner to {text}")
    ner = NerTransform.GetInfoAll(text)
    print(f"NER done : {ner}")
    retour = dataParse.parseSimple(ner)
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

@app.get("/predictA")
def PredictAll(text):
    ner = getNer(text)
    if(ner==None):
        #TODO gerer et monitorer l'erreur
        return None
    retour= ExtractFirstMeteo(ner)
    retour["weather_code"]=retour["weather_code"].apply(ReplaceCode)
    return retour.to_dict()



#Essai fonction fastAPi qui a besoin de javascript pour fonctionner
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    # Save the file temporarily
    file_path = f"temp_file.ogg"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    ogg_version = AudioSegment.from_ogg("temp_file.ogg")
    ogg_version.export("temp_audio.wav", format="wav")
    transcript = voice.recognize_from_file("temp_audio.wav")
    print(transcript)
    return {"transcription": transcript}

