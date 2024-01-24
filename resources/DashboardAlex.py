from flask import jsonify
from flask_restful import Resource
import json
from ratelimit import limits, sleep_and_retry

# Importiere die angepasste InstagrabiClient Klasse
from functions.main_instagrabi import InstagrabiClient


class FetchCardInfo(Resource):
    @sleep_and_retry
    @limits(calls=10, period=3600)  # Limitiere auf 10 Anfragen pro Stunde
    def get_instagram_data(self, username, password):
        # Initialisiere den Client mit Benutzername und Passwort
        client = InstagrabiClient(username, password)
        total_followers = client.get_profile_followers_count(username)
        total_followings = client.get_profile_followings_count(username)
        total_likes = client.get_total_likes(username)
        total_comments = client.get_total_comments(username)

        return total_likes, total_followers, total_comments, total_followings

    def get(self):
        json_file_path = 'database_clone/instagram_data.json'
        with open(json_file_path, 'r') as file:
            users = json.load(file)

        total_likes = 0
        total_followers = 0
        total_comments = 0
        total_followings = 0

        for user in users:
            if user['platform'] == 'Instagram':
                username = user['username']
                password = user['password']
                try:
                    likes, followers, comments, followings = self.get_instagram_data(username, password)
                    total_likes += likes
                    total_followers += followers
                    total_comments += comments
                    total_followings += followings
                except Exception as e:
                    print(f"Error fetching data for {username}: {e}")

        # Gibt die gesammelten Daten als JSON zurück
        return jsonify({
            'likesText': str(total_likes),
            'followerText': str(total_followers),
            'kommentarText': str(total_comments),
            'followingText': str(total_followings)
        })


