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

    def add_account(self, new_data):
        new_data['bot'] = new_data.get('bot', False)
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
            else:
                data = []

            data.append(new_data)

            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)

            return {'status': 'success'}, 200
        except (IOError, json.JSONDecodeError):
            return {'status': 'error', 'message': 'Fehler beim Speichern der Daten'}, 500

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
