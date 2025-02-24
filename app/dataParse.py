import dateparser
import requests
import datetime

def GetDateRange(listedate):
    if(len(listedate)==1):
        difference = listedate[0]-datetime.datetime.now()
        min = difference
        max = difference+1
        return(min,max)
    diffUn = listedate[0]-datetime.datetime.now()
    diffDeux = listedate[1]-datetime.datetime.now()
    if(diffDeux>diffUn):
        return(diffUn,diffDeux+1)
    else:
        return(diffUn,diffDeux+8)


def getDateSplit(text):
    #pour retirer les artefact ou dateparser attribut des valeurs étranges a des mots de liaison
    regular = ["de","a","et"]
    retour = []
    split = str.split(text)
    for cur in split:
        if(cur not in regular):
            retour.append(dateparser.parse(cur,settings={'PREFER_DATES_FROM': 'future'}))
    return retour

def getLL(localisation):
    requete = requests.get("https://api-adresse.data.gouv.fr/search/",params={"q":localisation})
    feat = requete.json()["features"]
    if(len(feat)==0):
        return None
    cord = feat[0]["geometry"]["coordinates"]
    long = cord[0]
    lat=cord[1]
    return {"latitude":lat,"longitude":long}


def parseSingleData(info):
    date = info["date"][0]
    date = dateparser.parse(date,settings={'PREFER_DATES_FROM': 'future'})
    info["date"]=date
    print(f"Date parsed : {date}")
    difference = date-datetime.datetime.now()
    info["difference"]=difference.days+1
    loc = info["loc"][0]
    requete = requests.get("https://api-adresse.data.gouv.fr/search/",params={"q":loc})
    cord = requete.json()["features"][0]["geometry"]["coordinates"]
    long = cord[0]
    lat=cord[1]
    print(f"Loc parsed :\nlattitude - {lat}\nlongitude - {long}")
    info["loc"]={"latitude":lat,"longitude":long}
    return info

def parseAll(info):
    retour={"date":None,"loc":None,"status":""}
    dateOk = True
    locOK = True
    #Idee : creer un retour pour voir les bug. avec un isbugged a false et si c'est le cas on renvoie le debug
    if(len(info["date"])==0):
        #TODO regarder le texte pour voir si il n'y a pas des oublie
        pass
    if(len(info["loc"])==0):
        #TODO traiter les cas ou on a pas trouver de localisation
        pass

    retour["date"]=[]
    for entre in info["date"]:
        parse = dateparser.parse(entre,settings={'PREFER_DATES_FROM': 'future'})
        #Traite le cas ou le parse ne marche pas
        if(parse==None):
            ajout = getDateSplit(entre)
            retour["date"].extend(ajout)
        else:
            retour["date"].append(parse)
    if(len(retour["date"])==0):
        dateOk=False

    retour["loc"]=[]
    for entre in info["loc"]:
        ajout = getLL(entre)
        if(ajout!=None):
            retour["loc"].append(ajout)
        else:
            #TODO
            pass

    if(len(retour["loc"])==0):
        locOK=False

    if(locOK and dateOk):
        retour["status"]="Success"
    elif((not locOK) and (not dateOk)):
        retour["status"]="ErDate/ErLoc"
    elif(not locOK):
        retour["status"]="ErLoc"
    else:
        retour["status"]="ErDate" 
    return retour