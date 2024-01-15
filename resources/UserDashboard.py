from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from database_clone import DataBase
from database_clone.DataBase import JsonDatabase
import json

from functions.main_instaloader import InstaloaderClient

db = JsonDatabase('database_clone/UserQuestionsDataBase.json')

class FetchChart(Resource):
    def get(self):
        # Annahme: Du hast bereits das Dictionary erstellt
        datensatz = {
            'visitors1': 40,
            'visitors2': 80,
            'visitors3': 20,
            'visitors4': 40,
            'visitors5': 60,
            'visitors6': 0,
            'visitors7': 100,
            'visitors8': 20,
            'visitors9': 60,
            'visitors10': 40
        }

        # Verwende jsonify, um das Dictionary als JSON zu formatieren und zurückzugeben
        return jsonify(datensatz)


class FetchChartPie(Resource):
    def get(self):
        # Annahme: Du speicherst den Text für Abschnitt 1 im Backend


        datensatz = {
            'Instagram': 40,
            'Facebook': 30,
            'TikTok': 20,
            'YouTube': 40,
        }


        return jsonify(datensatz)


from flask import jsonify

class FetchRecentInteractions(Resource):
    def get(self):
        try:
            # Define dropdown options
            account_options = ['Insta', 'Facebook', 'YouTube']
            account_group_options = ['Group 1', 'Group 2', 'Group 3']
            interaction_options = ['Likes', 'Followers', 'Views']

            # Logic to retrieve or calculate data based on selected values
            # ...

            # Construct response data
            data = {
                "account": account_options,
                "account_group": account_group_options,
                "interaction": interaction_options,
                # Include other data as needed
            }

            return jsonify(data)

        except Exception as e:
            return jsonify({"error": str(e)})



class FetchPerformingAccounts(Resource):
    def get(self):
        nameText = "Daviidoji"
        likesText = "176"

        return ({
            'nameText': nameText,
            'likesText': likesText
        })


class FetchAnswers(Resource):
    def get(self):
        data = db.get_all_answers()
        return jsonify(data)

class FetchCardInfo(Resource):
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
                client = InstaloaderClient(user['username'], user['password'])
                total_followers += client.get_profile_followers(user['username'])
                total_followings += client.get_profile_followings(user['username'])  # Followings hinzufügen
                posts = client.get_profile_posts(user['username'])
                for post in posts:
                    total_likes += post['likes']
                    total_comments += post['comment_count']

        likes_text = str(total_likes)
        follower_text = str(total_followers)
        kommentar_text = str(total_comments)
        following_text = str(total_followings)

        return jsonify({
            'likesText': likes_text,
            'followerText': follower_text,
            'kommentarText': kommentar_text,
            'followingText': following_text
        })

