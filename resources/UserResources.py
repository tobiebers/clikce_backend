from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from Classes.UserService import UserService
from database_clone.DataBase import JsonDatabase

db = JsonDatabase('database_clone/UserQuestionsDataBase.json')



class SubmitAnswers(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.get_json()

        # Überprüfen, ob Daten vorhanden sind
        if data is None:
            return {'message': 'Keine Daten übermittelt.'}, 400

        # Antworten einreichen und Ergebnis zurückgeben
        result = self.user_service.submit_answers(data)
        return result, 200

class ChangeAnswers(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.get_json()

        # Überprüfen der notwendigen Schlüssel in den Daten
        key = data.get('key')
        new_answer = data.get('answer')
        if key is None or new_answer is None:
            return {'message': 'Schlüssel und neue Antwort sind erforderlich.'}, 400

        # Antwort ändern und Ergebnis zurückgeben
        result = self.user_service.change_answer(key, new_answer)
        return result, 200

class SettingProfile(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.json

        # Überprüfen, ob alle erforderlichen Daten vorhanden sind
        required_fields = ['firstname', 'lastname', 'branche', 'language', 'password', 'goals', 'description']
        if not all(field in data for field in required_fields):
            return {'message': 'Alle Felder müssen ausgefüllt werden.'}, 400

        # Profil aktualisieren und Ergebnis zurückgeben
        result = self.user_service.update_profile(**data)
        return result, 200

class FetchAnswers(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def get(self):
        # Antworten abrufen und im JSON-Format zurückgeben
        data = self.user_service.fetch_answers()
        return jsonify(data)
