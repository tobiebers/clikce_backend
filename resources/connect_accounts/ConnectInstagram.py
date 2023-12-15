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



class InstagramProfileNames(Resource):
    def get(self):
        file_path = 'instagram_data.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                usernames = [user['username'] for user in data if 'username' in user]
                return {'usernames': usernames}, 200
        except (FileNotFoundError, json.JSONDecodeError):
            return {'usernames': []}, 200








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

        # JSON-Datei-Pfad
        file_path = 'instagram_data.json'

        # Vorhandene Daten lesen und aktualisieren
        try:
            with open(file_path, 'r') as file:
                # Existierende Daten laden
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Falls die Datei nicht existiert oder leer ist, ein neues leeres Array erstellen
            data = []

        # Neue Daten anhängen
        data.append(new_data)

        # Aktualisierte Daten in der Datei speichern
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return {'status': 'success'}, 200





from flask import request, jsonify
from flask_restful import Resource
import requests

class PostInstagramMedia(Resource):
    def post(self):
        access_token = load_token()  # Laden des gespeicherten Access Tokens
        if not access_token:
            return {'message': 'Token nicht gefunden'}, 404

        print(access_token)

        # Verwenden einer festen Bild-URL
        image_url = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fde.m.wikipedia.org%2Fwiki%2FDatei%3ABMW.svg&psig=AOvVaw2FOh8CRrwGKcYghMkel7O7&ust=1702566026839000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMCEsOrWjIMDFQAAAAAdAAAAABAD'  # Ersetzen Sie dies mit einer gültigen Bild-URL
        caption = request.json.get('caption')  # Bildunterschrift aus der Anfrage

        # Schritt 1: Erstellen eines Medienobjekts
        media_object_response = create_media_object(access_token, image_url, caption)
        if media_object_response.status_code != 200:
            return {'message': 'Fehler beim Erstellen des Medienobjekts'}, media_object_response.status_code

        media_id = media_object_response.json().get('id')

        # Schritt 2: Veröffentlichen des Medienobjekts
        publish_response = publish_media(access_token, media_id)
        if publish_response.status_code != 200:
            return {'message': 'Fehler beim Veröffentlichen des Beitrags'}, publish_response.status_code

        return {'message': 'Beitrag erfolgreich gepostet'}, 200

def create_media_object(access_token, image_url, caption):
    """Erstellt ein Medienobjekt auf Instagram."""
    url = f"https://graph.facebook.com/v14.0/me/media"
    payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    response = requests.post(url, data=payload)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code != 200:
        try:
            # Versuchen, die Fehlermeldung aus der Antwort zu extrahieren
            error_message = response.json().get('error', {}).get('message', 'Unbekannter Fehler')
        except ValueError:
            # Falls die Antwort keinen JSON-Inhalt hat
            error_message = response.text or 'Keine Fehlermeldung verfügbar'

        print("Fehler beim Erstellen des Medienobjekts:", error_message)
        return response

    return response


def publish_media(access_token, media_id):
    """Veröffentlicht ein Medienobjekt auf Instagram."""
    url = f"https://graph.facebook.com/v14.0/me/media_publish"
    payload = {
        'creation_id': media_id,
        'access_token': access_token
    }
    return requests.post(url, data=payload)

