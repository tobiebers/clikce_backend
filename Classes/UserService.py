class UserService:
    def __init__(self, db):
        self.db = db

    def fetch_answers(self):
        return self.db.get_all_answers()

    def change_answer(self, key, new_answer):
        self.db.update_answer(key, new_answer)
        return {'message': 'Antwort erfolgreich aktualisiert'}

    def login(self, email, password):
        # Hier würden Sie normalerweise die Authentifizierung implementieren
        print(f"Empfangene E-Mail: {email}")
        print(f"Empfangenes Passwort: {password}")
        return {'message': 'Daten empfangen', 'email': email, 'password': password}

    def submit_answers(self, answers):
        print("Erhaltene Antworten:", answers)
        self.db.add_answer(answers)
        return {'message': 'Antworten erfolgreich erhalten'}

    def update_profile(self, firstname, lastname, branche, language, password, goals, description):
        # Hier würde die Logik zur Aktualisierung des Profils implementiert werden
        print(f"Empfangene Daten: {firstname}, {lastname}, {branche}, {language}, {password}, {goals}, {description}")
        return {'message': 'Profil aktualisiert', 'data': {'firstname': firstname, 'lastname': lastname}}
