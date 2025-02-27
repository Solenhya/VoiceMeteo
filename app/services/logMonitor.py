import psycopg2
from dotenv import load_dotenv
import os
import datetime


class DataBaseManag:

    def __init__(self):
        connection = self.se_connecter_a_la_base_de_donnees()

    #Renvoi la connection ou None
    def se_connecter_a_la_base_de_donnees(self):
        load_dotenv()
        """Connexion à la base de données PostgreSQL."""
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        utilisateur = os.getenv("USER")
        mot_de_passe = os.getenv("PASSWORD")
        nom_base_de_donnees = "postgres"
        try:
            connexion = psycopg2.connect(
                dbname=nom_base_de_donnees,
                user=utilisateur,
                password=mot_de_passe,
                host=host,
                port=port
            )
            print("Connexion réussie à la base de données")
            return connexion
        except psycopg2.Error as e:
            print(f"Erreur lors de la connexion à la base de données: {e}")
            return None


    def LogConnectionAttempt(VoiceStatus,Text,NerStatus,meteoStatus):
        time = datetime.datetime.now()
