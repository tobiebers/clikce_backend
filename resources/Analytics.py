from flask import request, jsonify
from flask_restful import Resource
from ratelimit import sleep_and_retry, limits
from Classes.Analytics_Class import Analytics  # Stellen Sie sicher, dass Sie den korrekten Modulnamen verwenden

analytics = Analytics()  # Instanz der Analytics-Klasse

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
