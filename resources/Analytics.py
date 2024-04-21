from flask import request, jsonify
from flask_restful import Resource
from ratelimit import sleep_and_retry, limits
from Classes.Analytics_Class import Analytics
import json

analytics = Analytics()

class InstagramProfileData(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def post(self):
        req_data = request.get_json()
        username = req_data.get('username')

        if not username:
            return {'message': 'Kein Benutzername angegeben'}, 400

        profile_info, error = analytics.save_profile_info(username)
        if error:
            return {'message': error}, 404 if error == 'Anmeldedaten nicht gefunden' else 500

        return {'message': 'Daten erfolgreich gespeichert'}, 200

class SaveWeeklyData(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def post(self):
        try:
            analytics.save_weekly_data()
            return {'message': 'Wöchentliche Daten erfolgreich gespeichert'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

class SelectAccount(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def get(self, username):
        if not username:
            return {'message': 'Kein Benutzername angegeben'}, 400

        profile_info = analytics.get_profile_info(username)
        if not profile_info:
            return {'message': 'Profilinformationen nicht gefunden'}, 404

        return jsonify(profile_info)

class FetchLikesData(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def get(self):
        try:
            with open('database_clone/analytics_chart_information_likes.json', 'r') as file:
                likes_data = json.load(file)
            return jsonify(likes_data)
        except FileNotFoundError:
            return {'message': 'Likes-Daten nicht gefunden'}, 404
        except json.JSONDecodeError:
            return {'message': 'Fehler beim Lesen der Likes-Daten'}, 500

class FetchFollowerData(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)
    def get(self):
        try:
            with open('database_clone/analytics_user_information_follower.json', 'r') as file:
                follower_data = json.load(file)
            return jsonify(follower_data)
        except FileNotFoundError:
            return {'message': 'Follower-Daten nicht gefunden'}, 404
        except json.JSONDecodeError:
            return {'message': 'Fehler beim Lesen der Follower-Daten'}, 500


class LogResource(Resource):
    def get(self):
        log_file_path = 'log_file.json'  # Pfad zur JSON-Log-Datei

        # Lese die JSON-Datei
        try:
            with open(log_file_path, 'r', encoding='utf-8') as file:
                log_data = json.load(file)  # Liest direkt die Liste ein
        except FileNotFoundError:
            return {'error': 'Log file not found'}, 404
        except json.JSONDecodeError:
            return {'error': 'Error decoding JSON'}, 500
        except Exception as e:
            return {'error': str(e)}, 500

        # Gibt die Liste der Log-Einträge zurück
        return {'logs': log_data}