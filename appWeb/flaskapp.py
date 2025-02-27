import os
from flask import Flask, render_template

# Get the path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Set the template folder to the "templates" folder in the parent directory
app = Flask(__name__, template_folder=os.path.join(parent_dir, 'templates'))

@app.route("/") # Définition de la route pour la page d'accueil (/)
def index(): # Fonction associée à la route /
  return render_template("index.html", nom_app="Vocal Weather") # On charge le template index.html situé dans le dossier templates/, on passe la variable nom_app au template avec la valeur "Vocal Weather"

if __name__ == "__main__":
  app.run(debug=True) # Lancement du serveur de développement Flask en mode debug (utile pendant le développement)