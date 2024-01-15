from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from database_clone import DataBase
from database_clone.DataBase import JsonDatabase
from functions.main_instaloader import InstaloaderClient
import json
db = JsonDatabase('database_clone/UserQuestionsDataBase.json')

class Login(Resource):
    def post(self):
        data = request.json
        email = data.get('email')  # Empfängt die E-Mail aus dem Request
        password = data.get('password')  # Empfängt das Passwort aus dem Request

        print(f"Empfangene E-Mail: {email}")
        print(f"Empfangenes Passwort: {password}")

        return {'message': 'Daten empfangen', 'data': data}, 200

class SubmitAnswers(Resource):
    def post(self):
        data = request.get_json()
        print("Erhaltene Antworten:", data)
        db.add_answer(data)  # Speichern der Antwort
        print("Erhaltene Antworten:", data)
        return {'message': 'Antworten erfolgreich erhalten'}, 200

class ChangeAnswers(Resource):
    def post(self):
        data = request.get_json()
        key = data.get('key')  # Der Schlüssel für die Antwort (z.B. "0", "1", "2")
        new_answer = data.get('answer')  # Der neue Antworttext

        if key is not None and new_answer is not None:
            db.update_answer(key, new_answer)
            return {'message': 'Antwort erfolgreich aktualisiert'}, 200
        else:
            return {'message': 'Fehlende Daten'}, 400


class Settingprofil(Resource):
    def post(self):
        data = request.json

        firstname = data.get('firstname')  # Empfängt die E-Mail aus dem Request
        lastname= data.get('lastname')
        branche = data.get('branche')  # Empfängt die E-Mail aus dem Request
        language= data.get('language')
        password = data.get('password')  # Empfängt die E-Mail aus dem Request
        goals = data.get('goals')
        description = data.get('description')


        print(f"Empfangene vorname: {firstname}")
        print(f"Empfangenes nachname: {lastname}")
        print(f"Empfangene branche: {branche}")
        print(f"Empfangenes sprache: {language}")
        print(f"Empfangene password: {password}")
        print(f"Empfangenes ziele: {goals}")
        print(f"Empfangene beschreibung: {description}")



        return {'message': 'Daten empfangen', 'data': data}, 200

class FetchAnswers(Resource):
    def get(self):
        data = db.get_all_answers()
        return jsonify(data)



