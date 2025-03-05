# Application Vocal Weather
Application de prédiction météo a commande vocal avec un serveur fastAPI
## Prerequis

- Python version 3.11 (necessaire pour transformers)
- ffmpeg (necessaire pour la conversion audio)

## Installation

1. **Creer un  environement virtuel**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Installer requirements**
   ```
   pip install -r requirements.txt
   ```

3. **Installer ffmpeg**
   C'est necessaire pour la conversion audio
     Telecharger depuis [ffmpeg.org](https://ffmpeg.org/download.html) et ajouter au PATH

4. **Configure environment variables**
   - Copier le fichier exemple et renommer ".env"
   - Ouvrir `.env` et remplir les champs nescessaire

## Lancement
1. **Lancer l'environement virtuel**
```
venv\Scripts\activate
```
2. **Lancer le serveur fastAPI**
   ```
   python -m fastapi run main.py
   ```
3. **Attendre configuration STT,NER et base de donnée**
```
Setting configuration voice
Setting done
Création model Ner
Device set to use cpu
Modele charger
Connexion réussie à la base de données
Table valider
```