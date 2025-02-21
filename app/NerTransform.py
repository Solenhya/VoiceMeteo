
print("Création model Ner")
from transformers import CamembertTokenizer, AutoModelForTokenClassification
from transformers import pipeline
tokenizer = CamembertTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
NerPipeline = pipeline("ner",model=model,tokenizer=tokenizer,aggregation_strategy="simple")
print("Modele charger")


def GetNer(text):
    retour = NerPipeline(text)
    #Transform le numpy float en float
    for token in retour:
       token["score"]=token["score"].item()
    return retour

def ExtractInfoFromNer(ner):
    loc=[]
    date=[]
    for group in ner:
        if(group["entity_group"]=="DATE"):
            #And score et haut aussi ?
            date.append(group["word"])
        if(group["entity_group"]=="LOC"):
            loc.append(group["word"])
    return{"date":date,"loc":loc}
    
def GetInfoOne(text):
    retour = GetNer(text)
    info = ExtractInfoFromNer(retour)
    if(len(info["date"])>0 and len(info["loc"])>0):
        return {"date":info["date"][0],"loc":info["loc"][0]}
    else : 
        return None
    
def GetInfoAll(text):
    retour = GetNer(text)
    return ExtractInfoFromNer(retour)