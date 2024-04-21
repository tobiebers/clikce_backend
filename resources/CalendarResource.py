import glob
import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

from instabot import Bot

from Classes.CalendarService import CalendarService
from functions.post_schedule import get_credentials, get_image_path, load_user_data



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



class PlannedPosts(Resource):
    def __init__(self):
        self.service = CalendarService()

    def get(self):
        return self.service.get_planned_posts()


class PlanPost(Resource):
    def __init__(self):
        self.service = CalendarService()

    def post(self):
        if 'file' not in request.files:
            return {'error': 'Keine Datei hochgeladen'}, 400

        uploaded_file = request.files['file']
        date = request.form.get('date')
        time = request.form.get('time')
        account = request.form.get('accounts')
        caption = request.form.get('caption')

        return self.service.plan_post(uploaded_file, date, time, account, caption)


class CreateHashtagSet(Resource):
    def __init__(self):
        self.service = CalendarService()

    def post(self):
        data = request.get_json()
        return jsonify(self.service.create_hashtag_set(data.get('name'), data.get('hashtags')))

class GetHashtagSets(Resource):
    def __init__(self):
        self.service = CalendarService()

    def get(self):
        return jsonify(self.service.get_hashtag_sets())

