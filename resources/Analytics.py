from flask import request, jsonify
from flask_restful import Resource
import json
from ratelimit import sleep_and_retry, limits
from functions.main_instagrabi import InstagrabiClient

# Pfadangaben zu den Dateien
INSTAGRAM_CREDENTIALS_FILE = 'database_clone/instagram_data.json'
DATA_SAVE = 'database_clone/analytics_user_information.json'
LIKES_DATA_FILE = 'database_clone/analytics_chart_information_likes.json'
FOLLOWERS_DATA_FILE = 'database_clone/analytics_user_information_follower.json'


class InstagramProfileData(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def post(self):
        req_data = request.get_json()
        username = req_data.get('username')

        if not username:
            return {'message': 'Kein Benutzername angegeben'}, 400

        try:
            with open(INSTAGRAM_CREDENTIALS_FILE, 'r') as file:
                credentials = json.load(file)

            user_credentials = next((cred for cred in credentials if cred["username"] == username), None)
            if not user_credentials:
                return {'message': 'Anmeldedaten nicht gefunden'}, 404

            client = InstagrabiClient(user_credentials['username'], user_credentials['password'])
            profile_info = client.get_profile_info(username)

            with open(DATA_SAVE, 'r+') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
                data[username] = profile_info
                file.seek(0)
                json.dump(data, file, indent=4)

            # Keine Daten an das Frontend zurücksenden
            return {'message': 'Daten erfolgreich gespeichert'}, 200

        except Exception as e:
            return {'message': str(e)}, 500

class SaveWeeklyData(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def post(self):
        try:
            # Prozess zum Speichern wöchentlicher Daten für jeden Benutzer
            pass
        except Exception as e:
            return {'message': str(e)}, 500


class SelectAccount(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def get(self, username):
        if not username:
            return {'message': 'Kein Benutzername angegeben'}, 400

        try:
            with open(DATA_SAVE, 'r') as file:
                data = json.load(file)

            profile_info = data.get(username)
            if not profile_info:
                return {'message': 'Profilinformationen nicht gefunden'}, 404

            return jsonify(profile_info)

        except Exception as e:
            return {'message': str(e)}, 500


