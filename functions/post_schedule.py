from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import json
import os
import glob
from instabot import Bot  # Stelle sicher, dass du Bot von instabot importierst, nicht von deiner eigenen Klasse

# Pfad zum Verzeichnis des Skripts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Funktion, um den absoluten Pfad zur Bild-Datei zu bekommen
def get_image_path(relative_path):
    return os.path.join(BASE_DIR, *relative_path.strip("/").split("/"))


def job_function(post):
    # Lade Benutzerdaten
    users_data = load_user_data()
    if not users_data:
        print("Konnte Benutzerdaten nicht laden.")
        return

    # Bereinige den Accountnamen und holen die Anmeldeinformationen
    account_name = post['account'].strip('[]"')
    username, password = get_credentials(account_name, users_data)

    if username and password:
        print(f"Bereite vor, den Post zu veröffentlichen: {post['caption']} mit Bild {post['picture']} für Account {account_name}")

        # Lösche vorhandene Cookie-Dateien, um Login-Probleme zu vermeiden
        cookie_del = glob.glob("config/*cookie.json")
        for cookie_file in cookie_del:
            os.remove(cookie_file)

        # Instanziiere den InstaBot
        bot = Bot()

        # Führe die Login- und Upload-Operationen aus
        try:
            bot.login(username=username, password=password, is_threaded=True)
            picture_path = get_image_path(post['picture'])  # Generiere den absoluten Pfad
            print(f"Versuche, das Bild von {picture_path} hochzuladen")
            bot.upload_photo(picture_path, post['caption'])  # Verwende den absoluten Pfad

        except Exception as e:
            print(f"Fehler beim Hochladen des Posts: {e}")
        finally:
            bot.logout()

    else:
        print("Konnte Anmeldeinformationen für den Account nicht finden oder abrufen.")


def load_posts():
    try:
        with open('database_clone/planned_posts.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Fehler beim Laden der geplanten Posts:", e)
        return []

# Funktion zum Einrichten der geplanten Posts
def schedule_posts(scheduler, posts):
    for post in posts:
        post_time = datetime.datetime.strptime(f"{post['date']} {post['time']}", '%Y-%m-%d %H:%M')
        if post_time > datetime.datetime.now():
            scheduler.add_job(job_function, 'date', run_date=post_time, args=[post])

# Periodische Funktion zum Überprüfen auf neue Posts
def check_for_new_posts(scheduler):
    print("Überprüfe auf neue Posts...")
    posts = load_posts()
    schedule_posts(scheduler, posts)

# Hauptfunktion zum Einrichten des Schedulers
def setup_scheduler():
    scheduler = BackgroundScheduler()
    posts = load_posts()
    schedule_posts(scheduler, posts)

    # Füge einen periodischen Job hinzu, der alle 10 Minuten (oder einen anderen Intervall) nach neuen Posts sucht
    scheduler.add_job(lambda: check_for_new_posts(scheduler), 'interval', minutes=10)

    scheduler.start()


# Funktion, um Benutzername und Passwort für einen gegebenen Accountnamen zu holen
def get_credentials(account_name, users_data):
    for user in users_data:
        if user['username'] == account_name and user['platform'].lower() == 'instagram':
            return user['username'], user['password']
    print(f"Account '{account_name}' nicht gefunden oder nicht für Instagram.")
    return None, None

def load_user_data(filepath='database_clone/instagram_data.json'):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fehler beim Laden der Benutzerdaten: {e}")
        return None






