import dateparser
import requests
import datetime


#Une classe pour gerer des date quelle soit unique ou un range. Principale fontion de savoir si une entrer (mois,jour) et compris dans le format
class DateFormatCust:

    #Date est un dictionnaire avec "day" et "month"
    def __init__(self,firstDate,secondDate = None,type="Unique"):
        self.type = type
        self.firstDate = firstDate
        self.secondDate=secondDate
    
    def Correspond(self,day,month):
        if(self.type=="Unique"):
            if(day==self.firstDate["day"] and month == self.firstDate["month"]):
                return True
            else:
                return False
        if(self.type=="Range"):            
            supCond = ((day>=self.firstDate["day"] and month==self.firstDate["month"]) or (month > self.firstDate["month"]))
            infCond = ((day<=self.secondDate["day"] and month==self.secondDate["month"]) or (month<self.secondDate["month"]))
            if(supCond and infCond):
                return True
            else:
                return False


def GetDateRange(listedate):
    if(len(listedate)==1):
        difference = getDifference(listedate[0])
        min = difference
        max = difference+1
        return(min,max)
    diffUn = getDifference(listedate[0])
    diffDeux = getDifference(listedate[1])
    if(diffDeux>diffUn):
        return(diffUn,diffDeux+1)
    else:
        return(diffUn,diffDeux+8)

def getDifference(date):
    return (date-datetime.datetime.now()).days

def TraiteErreurDateParsing(text):
    """
    Les cas a traiter observer :
    -jeudi a Samedi : faire un split - enregister le "A" - traiter chaque input - renvoyer un range
    -samedi a jeudi : '' mais aussi gerer le fait que les date ne sont pas ordonner correctement
    -jeudi et samedi :  faire un split - enregister le "et" - traiter chaque input renvoyer deux date
    -Entre le jeudi et le samedi : '' ne pas enregister le "et" mais le "entre - renvoyer un range
    -Des date numerique non reconnue par exemple 'Le 20 Juin prochain' : TODO
    """


    #pour retirer les artefact ou dateparser attribut des valeurs étranges a des mots de liaison
    regular = ["de","a","et"]
    retour = []
    split = str.split(text)
    for cur in split:
        if(cur not in regular):
            parse = dateparser.parse(cur,settings={'PREFER_DATES_FROM': 'future'})
            if(parse!=None):
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

#Traite la localisation pour renvoyer une liste de dictionnaire avec longitude et lattitude
def TraiteLocalisation(info, retour):
    for entre in info["loc"]:
        ajout = getLL(entre)
        retour["locName"].append(entre)
        if(ajout!=None):
            retour["loc"].append(ajout)
        else:
            #TODO
            pass

#Traite les date pour renvoyer une liste de 
def TraiteDate(info, retour):
    for entre in info["date"]:
        parse = dateparser.parse(entre,settings={'PREFER_DATES_FROM': 'future'})
        #Traite le cas ou le parse ne marche pas
        if(parse==None):
            ajout = TraiteErreurDateParsing(entre)
            retour["date"].extend(ajout)
        else:
            firstDate = {"day":parse.day,"month":parse.month}
            retour["date"].append(DateFormatCust(firstDate=firstDate))

#Fonction pour parser toute les infos
def parseAll(info):
    retour={"date":None,"loc":None,"status":""}
    dateOk = True
    locOK = True
    retour["date"]=[]
    TraiteDate(info, retour)
    if(len(retour["date"])==0):
        dateOk=False

    retour["loc"]=[]
    TraiteLocalisation(info, retour)
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

def parseSimple(info):
    retour={"date":None,"loc":None,"status":""}
    dateOk = True
    locOK = True
    retour["date"]=[]
    TraiteDate(info, retour)
    if(len(retour["date"])==0):
        dateOk=False
    if(len(info["loc"])>0):
        retour["loc"]=info["loc"][0]
        toPrint = retour["loc"]
        print(f"localisation Trouver {toPrint}")
    else:
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