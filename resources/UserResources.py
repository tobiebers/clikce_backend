from flask import Flask, request
from flask_restful import Resource, Api

class Login(Resource):
    def post(self):
        data = request.json
        email = data.get('email')  # Empfängt die E-Mail aus dem Request
        password = data.get('password')  # Empfängt das Passwort aus dem Request

        print(f"Empfangene E-Mail: {email}")
        print(f"Empfangenes Passwort: {password}")

        return {'message': 'Daten empfangen', 'data': data}, 200

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