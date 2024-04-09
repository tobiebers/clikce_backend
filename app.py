# Flask-Restful-Klasse
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from config import Config
from flask_mail import Mail
from functions.post_schedule import setup_scheduler

#import von den klassen
from resources.UserResources import SubmitAnswers, FetchAnswers, ChangeAnswers
from resources.UserResources import SettingProfile
from resources.UserContact import Contact

#David
from resources.DashboardAlex import FetchPerformingAccounts, FetchRefreshData
#
#
#
#
#

#Tim
from resources.Analytics import InstagramProfileData, SaveWeeklyData, SelectAccount
from resources.connect_accounts.ConnectTikTok import TikTokAccountDetails
#
#
#

#Alex

from resources.DashboardAlex import FetchCardInfo
from resources.DashboardAlex import FetchChart
from resources.UserDashboard import FetchChartPie
from resources.DashboardDavid import FetchRecentInteractions, FetchRecentInteractionButton
#

#Tobi
from resources.connect_accounts.ConnectInstagram import AccountDetails, AddInstagramData, PostInstagramMedia, \
    DeleteAccount, FollowerCount, PlannedPosts, PlanPost, CreateHashtagSet, GetHashtagSets

from resources.connect_accounts.account_functions import CreateCaption, ScheduleBulkPosts, CreateBot

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
api.add_resource(SettingProfile, '/settingProfil')
api.add_resource(Contact, '/contact')
api.add_resource(SubmitAnswers, '/submit-answers')

#David
api.add_resource(FetchPerformingAccounts, '/fetch-performing-account')
api.add_resource(FetchRefreshData, '/fetch-refresh-data')
api.add_resource(FetchRecentInteractionButton, '/fetch-interaction-button')
#
#
#

#Tim
api.add_resource(InstagramProfileData, '/instagram-profile-data')
api.add_resource(SaveWeeklyData, '/save-weekly-data')
api.add_resource(SelectAccount, '/select-account/<string:username>')
api.add_resource(TikTokAccountDetails, '/tiktok-profiles')

#Alex
api.add_resource(FetchCardInfo, '/fetch-card-info')
api.add_resource(FetchChart, '/fetch-chart')
api.add_resource(FetchChartPie, '/fetch-chart-data')
api.add_resource(FetchRecentInteractions, '/fetch-recent-interactions')

#Tobi
api.add_resource(FetchAnswers, '/fetch-answers')
api.add_resource(ChangeAnswers, '/change-answers')





api.add_resource(PostInstagramMedia, '/instagram-post-picture')
api.add_resource(CreateCaption, '/create-caption')
api.add_resource(FollowerCount, '/followers/<string:username>')
api.add_resource(PlannedPosts, '/planned-posts')
api.add_resource(PlanPost, '/plan-post')
api.add_resource(ScheduleBulkPosts, '/schedule-bulk-posts')
api.add_resource(CreateBot, '/create-bot')
api.add_resource(CreateHashtagSet, '/create-hashtag-set')
api.add_resource(GetHashtagSets, '/get-hashtag-sets')


# User Resources
#api.add_resource(FetchAnswers, '/fetch-answers')
#api.add_resource(ChangeAnswers, '/change-answers')
#api.add_resource(Settingprofil, '/settingProfil')
#api.add_resource(Contact, '/contact')
#api.add_resource(SubmitAnswers, '/submit-answers')

# Acc-Man
api.add_resource(DeleteAccount, '/delete-account')
api.add_resource(AddInstagramData, '/instagram-profile-data')
api.add_resource(AccountDetails, '/instagram-profiles')



# Calandar resources



if __name__ == '__main__':
    setup_scheduler()
    app.run(debug=True)
