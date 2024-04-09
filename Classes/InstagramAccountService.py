import json
import os

class InstagramAccountService:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_accounts(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            accounts = [{'username': user['username'], 'platform': user.get('platform', 'Unknown')}
                        for user in data if 'username' in user]
            return {'accounts': accounts}, 200
        except (FileNotFoundError, json.JSONDecodeError):
            return {'accounts': []}, 200



    def delete_account(self, username):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            data = [account for account in data if account.get('username') != username]

            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)

            return {'status': 'success'}, 200
        except (FileNotFoundError, IOError, json.JSONDecodeError):
            return {'status': 'error', 'message': 'Fehler beim Aktualisieren der Daten'}, 500

        ''' def add_account(self, new_data):
             # Versuche, die vorhandene Datei zu öffnen und zu lesen, oder erstelle eine neue Liste
             if os.path.exists(self.file_path):
                 with open(self.file_path, 'r') as file:
                     try:
                         data = json.load(file)
                     except json.JSONDecodeError:
                         # Wenn ein JSONDecodeError auftritt, starte mit einer leeren Liste
                         data = []
             else:
                 data = []

             # Füge die neuen Daten zur Liste hinzu
             data.append(new_data)

             # Schreibe die aktualisierte Liste zurück in die Datei
             with open(self.file_path, 'w') as file:
                 json.dump(data, file, indent=4)

             return {'status': 'success'}, 200'''
