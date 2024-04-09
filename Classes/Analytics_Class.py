import json
from functions.main_instagrabi import InstagrabiClient

# Pfadangaben zu den Dateien
INSTAGRAM_CREDENTIALS_FILE = 'database_clone/instagram_data.json'
DATA_SAVE = 'database_clone/analytics_user_information.json'
LIKES_DATA_FILE = 'database_clone/analytics_chart_information_likes.json'
FOLLOWERS_DATA_FILE = 'database_clone/analytics_user_information_follower.json'


class Analytics:
    def get_user_credentials(self, username):
        with open(INSTAGRAM_CREDENTIALS_FILE, 'r') as file:
            credentials = json.load(file)
        return next((cred for cred in credentials if cred["username"] == username), None)

    def save_profile_info(self, username):
        user_credentials = self.get_user_credentials(username)
        if not user_credentials:
            return None, 'Anmeldedaten nicht gefunden'

        client = InstagrabiClient(user_credentials['username'], user_credentials['password'])
        profile_info = client.get_profile_info(username)

        with open(DATA_SAVE, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
            data[username] = profile_info
            file.seek(0)
            json.dump(data, file, indent=4)

        return profile_info, None

    def get_profile_info(self, username):
        with open(DATA_SAVE, 'r') as file:
            data = json.load(file)
        return data.get(username)

    def save_weekly_data(self):
        # Platzhalter für die Logik zum Speichern wöchentlicher Daten
        # Hier kann später die Implementierung hinzugefügt werden
        pass
