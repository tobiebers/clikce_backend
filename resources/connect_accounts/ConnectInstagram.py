import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json

from functions.main_instaloader import InstaloaderClient


class AccountDetails(Resource):
    def get(self):
        file_path = 'database_clone/instagram_data.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                accounts = [{'username': user['username'], 'platform': user.get('platform', 'Unknown')}
                            for user in data if 'username' in user]
                return {'accounts': accounts}, 200
        except (FileNotFoundError, json.JSONDecodeError):
            return {'accounts': []}, 200



class AddInstagramData(Resource):
    def post(self):
        new_data = request.get_json()
        file_path = 'database_clone/instagram_data.json'

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(new_data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return {'status': 'success'}, 200

class DeleteAccount(Resource):
    def post(self):
        username_to_delete = request.get_json().get('username')
        file_path = 'database_clone/instagram_data.json'

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'status': 'error', 'message': 'Datei nicht gefunden oder ungültiges JSON'}, 500

        data = [account for account in data if account.get('username') != username_to_delete]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return {'status': 'success'}, 200



class PostInstagramMedia(Resource):
    def post(self):
        # Zugriff auf die hochgeladene Datei
        uploaded_file = request.files['file']
        caption = request.form['caption']
        accounts = json.loads(request.form['accounts'])

        # Temporären Pfad der Datei ausgeben
        print("Empfangener Dateipfad:", uploaded_file.filename)

        # Speichern der Datei in einem bestimmten Verzeichnis (optional)
        save_path = os.path.join('static', uploaded_file.filename)
        uploaded_file.save(save_path)
        print("Datei gespeichert unter:", save_path)

        # Ausgeben der weiteren empfangenen Daten
        print("Caption:", caption)
        print("Accounts:", accounts)

        return {'status': 'success'}, 200


class FollowerCount(Resource):
    def get(self, username):
        client = InstaloaderClient()
        profile = client.get_profile(username)
        followers = client.get_profile_followers(profile)
        return {'followers': followers}


class PlannedPosts(Resource):
    def get(self):
        file_path = 'database_clone/planned_posts.json'
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    posts = json.load(file)
                return posts
            except json.JSONDecodeError as e:
                return {'error': 'JSON Decode Error: ' + str(e)}, 500
        else:
            return {'error': 'File not found: ' + file_path}, 404


class PlanPost(Resource):
    def post(self):
        # Zugriff auf die hochgeladene Datei
        if 'file' not in request.files:
            return {'error': 'Keine Datei hochgeladen'}, 400

        uploaded_file = request.files['file']

        # Extrahieren der anderen Daten aus der Anfrage
        date = request.form.get('date')
        time = request.form.get('time')
        account = request.form.get('accounts')
        caption = request.form.get('caption')

        # Temporären Pfad der Datei ausgeben und Datei speichern
        save_path = os.path.join('static', uploaded_file.filename)
        uploaded_file.save(save_path)

        # Erstellen eines neuen Post-Objekts
        new_post = {
            'date': date,
            'time': time,
            'account': account,
            'caption': caption,
            'picture': '/' + save_path.replace('\\', '/')
        }

        # JSON-File aktualisieren
        file_path = 'database_clone/planned_posts.json'
        if os.path.isfile(file_path):
            with open(file_path, 'r+') as file:
                posts = json.load(file)
                posts.append(new_post)
                file.seek(0)
                json.dump(posts, file, indent=4)
                file.truncate()
        else:
            with open(file_path, 'w') as file:
                json.dump([new_post], file, indent=4)

        return {'status': 'success'}, 200


