import streamlit as st
import requests
import pandas as pd
import json

def getMeteoSimple(latitude,longitude):
    res = requests.get("http://localhost:8000/meteo",params={"latitude":latitude,"longitude":longitude})
    print("status /meteo",res.status_code)
    data_dict = json.loads(res.json())

    return pd.DataFrame(data_dict)

def getVocalCommand():
    res = requests.get("http://localhost:8000/voice")
    print("vocal receive")
    return res.json()
getMeteoSimple(47.594246,0.465222)
if(st.button("Clic")):
    "Parlez"
    commande = getVocalCommand()
    st.write(f"Votre commande : {commande}")
    extraction = requests.get("http://localhost:8000/ner",params={"text":commande}).json()
    "Extraction"
    extraction
    "Fini"

ecritecom = st.text_input("Commande écrite")
if(st.button("Ecrit")):
    print(extraction = requests.get("http://localhost:8000/ner",params={"text":ecritecom}))