from flask import Flask, request
from flask_restful import Resource, Api

class Contact(Resource):
    def post(self):
        data = request.json
        first_name = data.get('vorname')
        last_name = data.get('nachname')
        email = data.get('email')
        phonenumber = data.get('handynummer')
        adress = data.get('adresse')
        country = data.get('land')
        password = data.get('passwort')

        print(f"Vorname: {first_name}")
        print(f"Nachname: {last_name}")
        print(f"E-Mail: {email}")
        print(f"Telefon Nummer: {phonenumber}")
        print(f"Adresse: {adress}")
        print(f"Land: {country}")
        print(f"Passwort: {password}")

        return {'message': 'Daten empfangen', 'data': data}, 200