# Flask-Restful-Klasse
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS


#import von den klassen
from resources.UserResources import Login
from resources.UserResources import Settingprofil
from resources.UserContact import Contact


#flask konfiguration
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Domains und Routen
api = Api(app)



#hinzufügen der routen
api.add_resource(Login, '/login')
api.add_resource(Settingprofil, '/settingProfil')
api.add_resource(Contact, '/contact')
if __name__ == '__main__':
    app.run(debug=True)
