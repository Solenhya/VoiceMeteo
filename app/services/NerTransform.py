
print("Création model Ner")
from transformers import CamembertTokenizer, AutoModelForTokenClassification
from transformers import pipeline
tokenizer = CamembertTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
NerPipeline = pipeline("ner",model=model,tokenizer=tokenizer,aggregation_strategy="simple")
print("Modele charger")


#Un service qui utilise un pipeline hugging face pour faire un NER et extraire toutes les date et localisation

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
            
    if (len(date)==0):
        #TODO regarder le texte pour voir si il n'y a pas des oublie
        pass
    if len(loc)==0:
        #TODO traiter les cas ou on a pas trouver de localisation
        pass
    return{"date":date,"loc":loc}

    
def GetInfoAll(text):
    retour = GetNer(text)
    return ExtractInfoFromNer(retour)