import json
from datetime import datetime
from Classes.Instagrapi_service import InstagrabiClient

# Pfadangaben zu den Dateien
INSTAGRAM_CREDENTIALS_FILE = 'database_clone/instagram_data.json'
DATA_SAVE = 'database_clone/analytics_user_information.json'
LIKES_DATA_FILE = 'database_clone/analytics_chart_information_likes.json'
FOLLOWERS_DATA_FILE = 'database_clone/analytics_user_information_follower.json'


class Analytics:
    def get_user_credentials(self, username):
        if not username:
            raise ValueError("Kein Benutzername angegeben.")
        with open(INSTAGRAM_CREDENTIALS_FILE, 'r') as file:
            credentials = json.load(file)
        return next((cred for cred in credentials if cred["username"] == username), None)

    def get_profile_info(self, username):
        if not username:
            raise ValueError("Kein Benutzername angegeben.")
        with open(DATA_SAVE, 'r') as file:
            data = json.load(file)
        return data.get(username)

    def custom_serializer(self, obj):
        """Konvertiert nicht-standard Objekte für JSON."""
        if hasattr(obj, 'isoformat'):  # Prüfe, ob es sich um ein Datumsobjekt handelt
            return obj.isoformat()
        # Füge weitere benutzerdefinierte Serialisierungen hier hinzu
        return str(obj)  # Als Fallback, konvertiere das Objekt zu einem String

    def save_profile_info(self, username):
        if not username:
            raise ValueError("Kein Benutzername angegeben.")
        user_credentials = self.get_user_credentials(username)
        if not user_credentials:
            return None, 'Anmeldedaten nicht gefunden'

        client = InstagrabiClient(user_credentials['username'], user_credentials['password'])
        profile_info = client.get_profile_info(username)
        top_post_details = client.get_top_post_details(username)

        with open(DATA_SAVE, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
            data[username] = {
                "profile_info": profile_info,
                "top_post": top_post_details
            }
            file.seek(0)
            # Verwende die custom_serializer Funktion für Objekte, die nicht direkt serialisiert werden können
            json.dump(data, file, indent=4, default=self.custom_serializer)

        return data[username], None

    def save_weekly_data(self):
        with open(INSTAGRAM_CREDENTIALS_FILE, 'r') as file:
            credentials = json.load(file)
        for cred in credentials:
            client = InstagrabiClient(cred['username'], cred['password'])
            profile_info = client.get_profile_info(cred['username'])

            # Speichere die aktuellen Follower- und Like-Zahlen
            self.save_data_to_file(FOLLOWERS_DATA_FILE, profile_info, "followers_count")
            self.save_data_to_file(LIKES_DATA_FILE, profile_info, "total_likes")

    def save_data_to_file(self, file_path, data, key):
        current_date = datetime.now().isoformat()
        entry = {"date": current_date, "value": data[key]}
        try:
            with open(file_path, 'r+') as file:
                file_data = json.load(file)
                file_data.append(entry)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        except json.JSONDecodeError:
            with open(file_path, 'w') as file:
                json.dump([entry], file, indent=4)
