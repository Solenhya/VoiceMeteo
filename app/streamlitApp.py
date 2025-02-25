import streamlit as st
import requests
import pandas as pd
import json


debugMode = False

def getMeteoSimple(latitude,longitude):
    res = requests.get("http://localhost:8000/meteo",params={"latitude":latitude,"longitude":longitude})
    print("status /meteo",res.status_code)
    data_dict = json.loads(res.json())

    return pd.DataFrame(data_dict)

def getVocalCommand():
    res = requests.get("http://localhost:8000/voice")
    print("vocal receive")
    return res.json()
#getMeteoSimple(47.594246,0.465222)
if(st.button("Clic")):
    "Parlez"
    commande = getVocalCommand()
    st.write(f"Votre commande : {commande}")
    requete = requests.get("http://localhost:8000/predictS",params={"text":commande})
    "Prediction"
    reqJson = requete.json()
    st.write(reqJson)
    st.write(f"{type(reqJson)}")
    for value , keys in reqJson.items():
        st.write(f"{keys} : {type(value)}") 
    "Fini"

ecritecom = st.text_input("Commande écrite")
if(st.button("Ecrit")):
    ner = requests.get("http://localhost:8000/nerInfo",params={"text":ecritecom})
    if(debugMode):
        st.write(ner)
        st.write(ner.json())
        st.write(type(ner.json()))
    prediction = requests.get("http://127.0.0.1:8000/predictA",params={"text":ecritecom})
    if(debugMode):
        st.write(prediction)
        st.write(prediction.json())
    data = pd.DataFrame(prediction.json())
    st.dataframe(data)
