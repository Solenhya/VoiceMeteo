import psycopg2
from dotenv import load_dotenv
import os
import datetime

tableTransc = """
CREATE TABLE IF NOT EXISTS monitoring.tabletranscription (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    code VARCHAR(100),
    transcription VARCHAR(500)
);
"""
tableNER = """
CREATE TABLE IF NOT EXISTS monitoring.tablener(
    id SERIAL PRIMARY KEY,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    code VARCHAR(100),
    date VARCHAR(100),
    localisation VARCHAR(500)
);
"""
tablePrevision="""
CREATE TABLE IF NOT EXISTS monitoring.tableprev(
    id SERIAL PRIMARY KEY,
    code VARCHAR(100),
    latitude VARCHAR(200),
    longitude VARCHAR(200)
)
"""

class DataBaseManag:

    def __init__(self):
        self.connection = self.se_connecter_a_la_base_de_donnees()
        self.CreateTables()
    #Renvoi la connection ou None
    def se_connecter_a_la_base_de_donnees(self):
        load_dotenv()
        """Connexion à la base de données PostgreSQL."""
        host = os.getenv("HOST")
        utilisateur = os.getenv("USER")
        mot_de_passe = os.getenv("PASSWORD")
        nom_base_de_donnees = "postgres"
        try:
            connexion = psycopg2.connect(
                dbname=nom_base_de_donnees,
                user=utilisateur,
                password=mot_de_passe,
                host=host
            )
            print("Connexion réussie à la base de données")
            return connexion
        except psycopg2.Error as e:
            print(f"Erreur lors de la connexion à la base de données: {e}")
            return None

    def CreateTables(self):
        curseur = self.connection.cursor()
        curseur.execute(tableTransc)
        curseur.execute(tableNER)
        curseur.execute(tablePrevision)
        self.connection.commit()
        curseur.close()
        print("Table valider")

    def LogTranscription(self,result,transcription):
        curseur = self.connection.cursor()
        transcripModifed = transcription.replace("'"," ")
        commande = f"INSERT INTO monitoring.tabletranscription (code,transcription) VALUES ('{result}','{transcripModifed}')"
        curseur.execute(commande)
        self.connection.commit()
        curseur.close()
        
    def logNer(self,retour):
        status = retour["status"]
        curseur = self.connection.cursor()
        if(status=="Success"):
            date = f"{retour['date'][0].firstDate['day']}/ {retour['date'][0].firstDate['month']}"
            localisation = retour["loc"]
            commande = f"INSERT INTO monitoring.tablener (code,date,localisation) VALUES ('{status}','{date}','{localisation}')"
        else:
            commande = f"INSERT INTO monitoring.tablener (code) VALUES ('{status}')"
        curseur.execute(commande)
        self.connection.commit()
        curseur.close()

    def logMeteo(sel,meteo):
        pass
    #TODO

    def LogConnectionAttempt(self,VoiceStatus,Text,NerStatus,commandeDate,localisation,meteoStatus):
        time = datetime.datetime.now()
