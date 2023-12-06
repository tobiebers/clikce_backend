from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json


IG_APP_ID = '2189358534587627'
IG_APP_SECRET = '1be29c4c32e05425188b44424df5adc3'
REDIRECT_URI = 'https://c105-95-115-104-211.ngrok-free.app/app/connectAccounts'

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



class InstagramProfileName(Resource):
    def get(self):
        access_token = load_token()
        if not access_token:
            return {'message': 'Token nicht gefunden'}, 404

        profile_url = f"https://graph.instagram.com/me?fields=username&access_token={access_token}"
        response = requests.get(profile_url)

        if response.status_code != 200:
            return {'message': 'Fehler beim Abrufen des Profilnamens'}, response.status_code

        profile_data = response.json()
        return {'username': profile_data.get('username', 'Nicht verfügbar')}








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
    def get(self):
        try:
            with open('instagram_token.json', 'r') as file:
                data = json.load(file)
            return data, 200
        except FileNotFoundError:
            return {'message': 'Daten nicht gefunden'}, 404



