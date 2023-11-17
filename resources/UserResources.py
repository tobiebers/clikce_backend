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