from flask import jsonify
from flask_restful import Resource
import json
from ratelimit import limits, sleep_and_retry
from functions.main_instagrabi import InstagrabiClient
from flask import request

class FetchRecentInteractions(Resource):
    def get(self):
        try:
            # Pfad zur JSON-Datei
            json_file_path = 'database_clone/alex_data.json'

            # Laden der JSON-Daten aus der Datei
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)

            # Extrahieren einzigartiger Plattformen
            platforms = {entry["platform"] for entry in json_data}

            # Extrahieren einzigartiger Benutzernamen für account_group_options
            account_groups = {entry["username"] for entry in json_data}

            # Definieren der Dropdown-Optionen
            account_options = list(platforms)  # Verwenden Sie die extrahierten Plattformen
            account_group_options = list(account_groups)  # Verwenden Sie die extrahierten Benutzernamen
            interaction_options = ['Likes', 'Followers', 'Followings', 'Comments']

            # Konstruieren der Antwortdaten
            data = {
                "account": account_options,
                "account_group": account_group_options,
                "interaction": interaction_options,
                # Weitere Daten nach Bedarf einfügen!
            }

            return jsonify(data)

        except Exception as e:
            return jsonify({"error": str(e)})



class FetchRecentInteractionButton(Resource):
    def get_user_selections(self):
        # Hier sollten Sie die Benutzerauswahl aus dem Request erhalten
        # Für das Beispiel verwende ich feste Werte
        selected_account = request.args.get('account')
        selected_account_group = request.args.get('account_group')
        selected_interaction = request.args.get('interaction')

        return selected_account, selected_account_group, selected_interaction

    def find_interaction_data(self, account, account_group, interaction):
        json_file_path = 'database_clone/alex_data.json'
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        for entry in json_data:
            if entry['username'] == account_group and entry['platform'] == account:
                return entry.get(interaction, 0)  # Gibt 0 zurück, falls der Schlüssel nicht existiert

        return "Keine Daten gefunden"

    def get(self):
        account, account_group, interaction = self.get_user_selections()
        interaction_value = self.find_interaction_data(account, account_group, interaction)
        return jsonify({interaction: interaction_value})