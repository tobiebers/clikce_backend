import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json
import glob
from instabot import Bot

from Classes.InstagramAccountService import InstagramAccountService
from functions.post_schedule import get_credentials, get_image_path, load_user_data

from functions.main_instaloader import InstaloaderClient


class AccountDetails(Resource):
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def get(self):
        return self.service.get_accounts()


class AddInstagramData(Resource):
    def post(self):
        # Empfangene Daten ausgeben
        new_data = request.get_json()
        print("Empfangene Daten:", new_data)  # Debug-Print der empfangenen Daten

        # Standardmäßig 'bot' auf False setzen, falls nicht angegeben
        new_data['bot'] = new_data.get('bot', False)

        # Pfad zur Datei definieren
        file_path = 'database_clone/instagram_data.json'

        # Existierende Daten aus der Datei lesen oder eine leere Liste initialisieren
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        # Neue Daten hinzufügen
        data.append(new_data)

        # Neue Daten in die Datei schreiben
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify({'status': 'success'}), 200

class DeleteAccount(Resource):
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def post(self):
        username = request.get_json().get('username')
        return self.service.delete_account(username)


class FollowerCount(Resource):
    def get(self, username):
        client = InstaloaderClient()
        profile = client.get_profile(username)
        followers = client.get_profile_followers(profile)
        return {'followers': followers}






