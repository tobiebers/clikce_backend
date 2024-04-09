import json
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

    def save_profile_info(self, username):
        if not username:
            raise ValueError("Kein Benutzername angegeben.")
        user_credentials = self.get_user_credentials(username)
        if not user_credentials:
            return None, 'Anmeldedaten nicht gefunden'

        client = InstagrabiClient(user_credentials['username'], user_credentials['password'])
        profile_info = client.get_profile_info(username)
        top_post_details = self.get_top_post_details(username)  # Holen der Top-Post-Daten

        with open(DATA_SAVE, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
            # Hinzufügen der Top-Post-Daten zu den Profilinformationen
            data[username] = {
                "profile_info": profile_info,
                "top_post": top_post_details
            }
            file.seek(0)
            json.dump(data, file, indent=4)

        return data[username], None


    def save_weekly_data(self):
        # Platzhalter für die Logik zum Speichern wöchentlicher Daten
        # Hier kann später die Implementierung hinzugefügt werden
        pass
