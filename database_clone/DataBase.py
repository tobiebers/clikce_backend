import json
import os

class JsonDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.initialize_database()

    def initialize_database(self):
        if not os.path.exists(self.filename):
            try:
                self.write_data([])  # Initialisiere mit leerem Array
            except FileNotFoundError as e:
                # Ausgabe des aktuellen Arbeitsverzeichnisses und des erwarteten Dateipfads
                current_dir = os.getcwd()
                expected_path = os.path.abspath(self.filename)
                print(f"Fehler: {e}")
                print(f"Das aktuelle Arbeitsverzeichnis ist {current_dir}")
                print(f"Erwarteter vollständiger Pfad der Datei: {expected_path}")
                print("Bitte überprüfe, ob der Pfad korrekt ist und die Datei existiert.")
                raise

    def read_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # oder einen anderen geeigneten Standardwert

    def write_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def add_answer(self, answer):
        data = self.read_data()
        data.append(answer)
        self.write_data(data)


    def delete_answer(self, answer_id):
        data = self.read_data()
        data = [answer for answer in data if answer['id'] != answer_id]
        self.write_data(data)

    def update_answer(self, key, new_answer):
        data = self.read_data()
        if len(data) > 0:
            data[0][key] = new_answer  # Aktualisiere die Antwort anhand des Schlüssels
        else:
            data.append({key: new_answer})  # Füge hinzu, wenn keine Daten vorhanden sind
        self.write_data(data)

    def get_all_answers(self):
        return self.read_data()
