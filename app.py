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
from resources.UserDashboard import FetchPerformingAccounts
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
from resources.UserDashboard import FetchChart
from resources.UserDashboard import FetchChartPie
from resources.UserDashboard import FetchRecentInteractions
#

#Tobi
from resources.connect_accounts.ConnectInstagram import AccountDetails, InstagramData, PostInstagramMedia, \
    DeleteAccount, FollowerCount, PlannedPosts

from resources.connect_accounts.account_functions import CreateCaption
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
api.add_resource(FetchPerformingAccounts, '/fetch-performing-account')
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
api.add_resource(FetchChart, '/fetch-chart')
api.add_resource(FetchChartPie, '/fetch-chart-data')
api.add_resource(FetchRecentInteractions, '/fetch-recent-interactions')
#

#Tobi
api.add_resource(FetchAnswers, '/fetch-answers')
api.add_resource(ChangeAnswers, '/change-answers')
api.add_resource(DeleteAccount, '/delete-account')
api.add_resource(AccountDetails, '/instagram-profiles')
api.add_resource(InstagramData, '/instagram-profile-data')
api.add_resource(PostInstagramMedia, '/instagram-post-picture')
api.add_resource(CreateCaption, '/create-caption')
api.add_resource(FollowerCount, '/followers/<string:username>')
api.add_resource(PlannedPosts, '/planned-posts')



if __name__ == '__main__':
    app.run(debug=True)
