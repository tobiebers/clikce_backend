from flask import jsonify
from flask_restful import Resource
import json
from ratelimit import limits, sleep_and_retry
from Classes.Instagrapi_service import InstagrabiClient
from datetime import datetime

@sleep_and_retry
@limits(calls=10, period=3600)
def collect_and_store_instagram_data():
    json_input_file_path = 'database_clone/instagram_data.json'
    json_output_file_path = 'database_clone/alex_data.json'
    json_chart_output_file_path = 'database_clone/chart_dashboard.json'

    # Daten aus der Eingabedatei lesen
    with open(json_input_file_path, 'r') as file:
        users = json.load(file)

    collected_data = []
    total_likes = 0
    today = datetime.now().strftime('%d-%m')

    # Daten für jeden Benutzer sammeln
    for user in users:
        if user['platform'] == 'Instagram':
            client = InstagrabiClient(user['username'], user['password'])
            user_data = {
                "username": user['username'],
                "platform": user['platform'],
                "likes": client.get_total_likes(user['username']),
                "followers": client.get_profile_followers_count(user['username']),
                "comments": client.get_total_comments(user['username']),
                "followings": client.get_profile_followings_count(user['username'])
            }
            collected_data.append(user_data)
            total_likes += user_data['likes']

    # Gesammelte Daten in einer neuen JSON-Datei speichern
    with open(json_output_file_path, 'w') as file:
        json.dump(collected_data, file)

    # Vorhandene Daten aus chart_dashboard.json lesen
    try:
        with open(json_chart_output_file_path, 'r') as file:
            existing_chart_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_chart_data = []

    # Fügen Sie die neuen Daten hinzu
    chart_data = {"date": today, "total_likes": total_likes}
    existing_chart_data.append(chart_data)

    # Aktualisierte Liste in die Datei schreiben
    with open(json_chart_output_file_path, 'w') as file:
        json.dump(existing_chart_data, file)

    print("JSON-Dateien erfolgreich aktualisiert.")




class FetchRefreshData(Resource):
    def get(self):
        try:
            collect_and_store_instagram_data()
            return {'message': 'Daten erfolgreich aktualisiert'}, 200
        except Exception as e:
            return {'message': str(e)}, 500


class FetchCardInfo(Resource):
    def get(self):
        json_file_path = 'database_clone/alex_data.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        total_likes = sum(user_data['likes'] for user_data in data)
        total_followers = sum(user_data['followers'] for user_data in data)
        total_comments = sum(user_data['comments'] for user_data in data)
        total_followings = sum(user_data['followings'] for user_data in data)

        return jsonify({
            'likesText': str(total_likes),
            'followerText': str(total_followers),
            'kommentarText': str(total_comments),
            'followingText': str(total_followings)
        })




class FetchPerformingAccounts(Resource):
    def get(self):
        json_file_path = 'database_clone/alex_data.json'

        with open(json_file_path, 'r') as file:
            users = json.load(file)

        max_likes = 0
        max_likes_username = ''

        for user in users:
            likes = user['likes']
            if likes > max_likes:
                max_likes = likes
                max_likes_username = user['username']
                # Fügen Sie hier Logik für das Profilbild hinzu, falls erforderlich

        return jsonify({
            'nameText': "Name: " + max_likes_username,
            'likesText': "Likes: " + str(max_likes),
            'profilePicture': 'Placeholder.jpg'
        })



class FetchChart(Resource):
    def get(self):
        # Pfad zur JSON-Datei
        json_file_path = 'database_clone/chart_dashboard.json'

        # JSON-Datei lesen
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Nehmen Sie die letzten 10 Einträge, falls mehr vorhanden sind
        data = data[-10:]

        # Verwenden Sie jsonify, um die Liste als JSON zu formatieren und zurückzugeben
        return jsonify(data)



