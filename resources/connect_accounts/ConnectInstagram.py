import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json


IG_APP_ID = '355339213741957'
IG_APP_SECRET = '05fc1d2e6861936e33c1d597abdc9b9e'
REDIRECT_URI = 'https://0d80-2a01-c23-c1ed-7000-fc08-8be0-d562-319a.ngrok-free.app/app/connectAccounts'

class ConnectInsta(Resource):
    def get(self):
        auth_url = (
            f"https://api.instagram.com/oauth/authorize"
            f"?client_id={IG_APP_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope=user_profile,user_media"
            f"&response_type=code"
        )
        return jsonify(authUrl=auth_url)


class ConvertCode(Resource):
    def post(self):
        # Abrufen des Codes aus der Anfrage
        code = request.json.get('code')

        # Erstellen des Payloads für die Tokenanfrage
        payload = {
            'client_id': IG_APP_ID,
            'client_secret': IG_APP_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'code': code
        }

        # Anfrage an Instagram, um den Access Token zu erhalten
        response = requests.post('https://api.instagram.com/oauth/access_token', data=payload)

        # Debug-Ausgabe der Antwort
        print("Instagram API Response:", response.status_code, response.text)

        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code != 200:
            return {'message': 'Fehler bei der Tokenanfrage'}, response.status_code

        # Extrahieren des Access Tokens aus der Antwort
        data = response.json()
        access_token = data.get('access_token')

        # Abrufen des Benutzernamens mit dem erhaltenen Token
        username = self.get_username(access_token)

        if username:
            # Speichern des Tokens mit Benutzername und Kontotyp
            save_token(access_token, username)
            return {'message': 'Token und Benutzername gespeichert'}, 200
        else:
            return {'message': 'Fehler beim Abrufen des Benutzernamens'}, 400

    def get_username(self, token):
        """Holt den Instagram-Benutzernamen mit dem gegebenen Token."""
        profile_url = f"https://graph.instagram.com/me?fields=username&access_token={token}"
        response = requests.get(profile_url)
        if response.status_code == 200:
            profile_data = response.json()
            return profile_data.get('username')
        return None



class AccountDetails(Resource):
    def get(self):
        file_path = 'instagram_data.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                accounts = [{'username': user['username'], 'platform': user.get('platform', 'Unknown')}
                            for user in data if 'username' in user]
                return {'accounts': accounts}, 200
        except (FileNotFoundError, json.JSONDecodeError):
            return {'accounts': []}, 200








def save_token(token, username):
    """Speichert den Token mit zusätzlichen Informationen."""
    data = {
        'instatoken': token,
        'username': username,
        'type': 'Instagram'
    }
    with open('instagram_token.json', 'w') as file:
        json.dump(data, file)
    print("Token und Benutzername gespeichert:", token, username)


def load_token():
    try:
        with open('instagram_token.json', 'r') as file:
            data = json.load(file)
            return data.get('instatoken')
    except FileNotFoundError:
        return None



class InstagramData(Resource):
    def post(self):
        new_data = request.get_json()
        file_path = 'instagram_data.json'

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(new_data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return {'status': 'success'}, 200






from flask import request, jsonify
from flask_restful import Resource
import requests

class PostInstagramMedia(Resource):
    def post(self):
        # Zugriff auf die hochgeladene Datei
        uploaded_file = request.files['file']
        caption = request.form['caption']
        accounts = json.loads(request.form['accounts'])

        # Temporären Pfad der Datei ausgeben
        print("Empfangener Dateipfad:", uploaded_file.filename)

        # Speichern der Datei in einem bestimmten Verzeichnis (optional)
        save_path = os.path.join('resources/connect_accounts/pictures', uploaded_file.filename)
        uploaded_file.save(save_path)
        print("Datei gespeichert unter:", save_path)

        # Ausgeben der weiteren empfangenen Daten
        print("Caption:", caption)
        print("Accounts:", accounts)

        return {'status': 'success'}, 200

