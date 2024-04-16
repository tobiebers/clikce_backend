import os
import json
from glob import glob

class CalendarService:
    def __init__(self):
        self.post_directory = 'static'
        self.instagram_data_file = 'database_clone/instagram_data.json'
        self.planned_posts_file = 'database_clone/planned_posts.json'  # Pfad zur Datei mit geplanten Posts
        self.hashtag_sets_file = 'database_clone/hashtag_sets.json'    # Pfad zur Datei mit Hashtag-Sets




    def post_instagram_media(self, uploaded_file, caption, accounts):
        # Temporären Pfad der Datei ausgeben
        print("Empfangener Dateipfad:", uploaded_file.filename)

        # Speichern der Datei in einem bestimmten Verzeichnis (optional)
        save_path = os.path.join(self.post_directory, uploaded_file.filename)
        uploaded_file.save(save_path)
        print("Datei gespeichert unter:", save_path)

        # Ausgeben der weiteren empfangenen Daten
        print("Caption:", caption)
        print("Accounts:", accounts)

        # Hier könnte die Logik zur Interaktion mit Instagram-APIs stehen
        # Zum Beispiel das Posten des Bildes auf Instagram
        # Dies ist aktuell simuliert durch Ausgabe auf der Konsole

        # Für jeden Account in der Liste
        for account_name in accounts:
            print(f"Bereite vor, den Post zu veröffentlichen für Account {account_name}")

        # Erfolgsmeldung zurückgeben
        return {'status': 'success'}, 200

    def get_planned_posts(self):
        # Versuch, die geplanten Posts aus der JSON-Datei zu lesen
        if os.path.isfile(self.planned_posts_file):
            try:
                with open(self.planned_posts_file, 'r') as file:
                    posts = json.load(file)
                return posts
            except json.JSONDecodeError as e:
                return {'error': 'JSON Decode Error: ' + str(e)}, 500
        else:
            return {'error': 'File not found: ' + self.planned_posts_file}, 404


    def plan_post(self, uploaded_file, date, time, account, caption):
        # Überprüfung und Speicherung der hochgeladenen Datei
        save_path = os.path.join(self.post_directory, uploaded_file.filename)
        uploaded_file.save(save_path)

        # Erstellen eines neuen Post-Objekts
        new_post = {
            'date': date,
            'time': time,
            'account': account,
            'caption': caption,
            'picture': '/' + save_path.replace('\\', '/')
        }

        # Aktualisieren der JSON-Datei mit den geplanten Posts
        if os.path.isfile(self.planned_posts_file):
            with open(self.planned_posts_file, 'r+') as file:
                posts = json.load(file)
                posts.append(new_post)
                file.seek(0)
                json.dump(posts, file, indent=4)
                file.truncate()
        else:
            with open(self.planned_posts_file, 'w') as file:
                json.dump([new_post], file, indent=4)

        return {'status': 'success'}, 200


    def create_hashtag_set(self, name, hashtags):
        try:
            if not os.path.isfile(self.hashtag_sets_file) or os.path.getsize(self.hashtag_sets_file) == 0:
                existing_sets = []
            else:
                with open(self.hashtag_sets_file, 'r') as file:
                    existing_sets = json.load(file)

            existing_sets.append({
                'name': name,
                'hashtags': hashtags
            })

            with open(self.hashtag_sets_file, 'w') as file:
                json.dump(existing_sets, file, indent=4)

            return {'status': 'success', 'message': 'Hashtag-Set erstellt'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_hashtag_sets(self):
        try:
            with open(self.hashtag_sets_file, 'r') as file:
                hashtag_sets = json.load(file)
            return {'hashtagSets': hashtag_sets}
        except (FileNotFoundError, json.JSONDecodeError):
            return {'status': 'error', 'message': 'Keine Hashtag-Sets gefunden'}



