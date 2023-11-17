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


class Einstellungprofil(Resource):
    def post(self):
        data = request.json

        vorname = data.get('vorname')  # Empfängt die E-Mail aus dem Request
        nachname = data.get('nachname')
        branche = data.get('branche')  # Empfängt die E-Mail aus dem Request
        sprache = data.get('sprache')
        password = data.get('password')  # Empfängt die E-Mail aus dem Request
        ziele = data.get('ziele')
        beschreibung = data.get('beschreibung')


        print(f"Empfangene vorname: {vorname}")
        print(f"Empfangenes nachname: {nachname}")
        print(f"Empfangene branche: {branche}")
        print(f"Empfangenes sprache: {sprache}")
        print(f"Empfangene password: {password}")
        print(f"Empfangenes ziele: {ziele}")
        print(f"Empfangene beschreibung: {beschreibung}")



        return {'message': 'Daten empfangen', 'data': data}, 200
