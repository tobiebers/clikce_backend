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
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def post(self):
        new_data = request.get_json()
        return self.service.add_account(new_data)

class DeleteAccount(Resource):
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def post(self):
        username = request.get_json().get('username')
        return self.service.delete_account(username)




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

        # Für jeden Account in der Liste
        for account_name in accounts:
            # Bereinige den Accountnamen und hole die Anmeldeinformationen
            username, password = get_credentials(account_name, load_user_data())

            if username and password:
                print(f"Bereite vor, den Post zu veröffentlichen für Account {account_name}")

                # Erstelle eine Instanz des Bots
                bot = Bot()

                try:
                    # Generiere den absoluten Pfad zur Bilddatei
                    picture_path = get_image_path(save_path)
                    # Lösche vorhandene Cookie-Dateien, um Login-Probleme zu vermeiden
                    cookie_del = glob.glob("config/*cookie.json")
                    for cookie_file in cookie_del:
                        os.remove(cookie_file)

                    # Führe die Login- und Upload-Operationen aus
                    bot.login(username=username, password=password, is_threaded=True)
                    bot.upload_photo(picture_path, caption)

                except Exception as e:
                    print(f"Fehler beim Hochladen des Posts: {e}")
                finally:
                    bot.logout()
            else:
                print(f"Konnte Anmeldeinformationen für den Account {account_name} nicht finden oder abrufen.")

        return {'status': 'success'}, 200

#


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

class CreateHashtagSet(Resource):
    def post(self):
        try:
            data = request.get_json()
            print(data)  # Zum Debuggen

            name = data.get('name')
            hashtags = data.get('hashtags')

            file_path = 'database_clone/hashtag_sets.json'

            # Stellen Sie sicher, dass die Datei existiert und gültiges JSON enthält
            if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
                existing_sets = []
            else:
                with open(file_path, 'r') as file:
                    existing_sets = json.load(file)

            existing_sets.append({
                'name': name,
                'hashtags': hashtags
            })

            with open(file_path, 'w') as file:
                json.dump(existing_sets, file, indent=4)

            return jsonify({'status': 'success', 'message': 'Hashtag-Set erstellt'})

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


class GetHashtagSets(Resource):
    def get(self):
        try:
            with open('database_clone/hashtag_sets.json', 'r') as file:
                hashtag_sets = json.load(file)
            return jsonify({'hashtagSets': hashtag_sets})
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({'status': 'error', 'message': 'Keine Hashtag-Sets gefunden'}), 404