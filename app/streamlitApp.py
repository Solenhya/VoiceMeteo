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
    extraction = requests.get("http://localhost:8000/predictA",params={"text":ecritecom})
    print(extraction.json())
    data = pd.DataFrame(json.loads(extraction.json()))
    st.dataframe(data)
    st.write(extraction.json())
if(st.button("Meteo")):
    requete = requests.get("http://localhost:8000/meteo")
    st.write(requete.json())