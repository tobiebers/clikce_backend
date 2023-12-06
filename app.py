# Flask-Restful-Klasse
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from config import Config
from flask_mail import Mail

#import von den klassen
from resources.UserResources import Login, SubmitAnswers, FetchAnswers, ChangeAnswers
from resources.UserResources import Settingprofil
from resources.UserContact import Contact

#David
#
#
#
#
#
#

#Tim
#
#
#
#
#
#

#Alex

from resources.UserResources import FetchCardInfo
#
#
#
#

#Tobi
from resources.connect_accounts.ConnectInstagram import ConnectInsta, ConvertCode, InstagramProfileName, InstagramData

#
#
#
#
#



#flask konfiguration
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Domains und Routen
api = Api(app)
app.config.from_object(Config)
mail = Mail(app)
#app.config.from_object(Config)  # Lädt Konfiguration aus der Config-Klasse




#hinzufügen der routen
api.add_resource(Login, '/login')
api.add_resource(Settingprofil, '/settingProfil')
api.add_resource(Contact, '/contact')
api.add_resource(SubmitAnswers, '/submit-answers')

#David
#
#
#
#
#
#

#Tim
#
#
#
#
#
#

#Alex
api.add_resource(FetchCardInfo, '/fetch-card-info')
#
#
#
#

#Tobi
api.add_resource(FetchAnswers, '/fetch-answers')
api.add_resource(ChangeAnswers, '/change-answers')
api.add_resource(ConnectInsta, '/connect-instagram')
api.add_resource(ConvertCode, '/convert-code')
api.add_resource(InstagramProfileName, '/instagram-profile-name')
api.add_resource(InstagramData, '/instagram-profile-data')
#


if __name__ == '__main__':
    app.run(debug=True)
