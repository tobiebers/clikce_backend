from flask import jsonify
from flask_restful import Resource
import json

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
    def post(self):
        # Extrahiere die JSON-Daten aus dem Body der Anfrage
        json_data = request.get_json(force=True)

        # Zum Debuggen: Ausgabe der empfangenen Daten
        print("Empfangene Daten:", json_data)

        # Sicherstellen, dass die benötigten Schlüssel vorhanden sind
        if 'account' in json_data and 'accountGroup' in json_data and 'interaction' in json_data:
            account = json_data['account']
            account_group = json_data['accountGroup']
            interaction = json_data['interaction']

            # Rufe die Funktion find_interaction_data mit den empfangenen Daten auf
            interaction_count = self.find_interaction_data(account, account_group, interaction.lower())

            # Sende eine Antwort zurück mit den gefundenen Daten
            return jsonify({'interaction_count': interaction_count})
        else:
            return jsonify({'error': 'Fehlende oder ungültige Daten in der Anfrage'}), 400

    def find_interaction_data(self, account, account_group, interaction):
        json_file_path = 'database_clone/alex_data.json'
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        for entry in json_data:
            if entry['username'] == account_group and entry['platform'].lower() == account.lower():
                # Achte auf die Groß- und Kleinschreibung des Interaktionsschlüsselss
                interaction_count = entry.get(interaction, "Keine Daten gefunden")
                print("interaction:", interaction, interaction_count)
                return interaction_count

        return "Keine Daten gefunden"

