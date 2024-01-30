from flask_restful import Resource, Api
import json

class TikTokAccountDetails(Resource):
    def get(self):
        file_path = 'database_clone/tiktok_data.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                accounts = [{'username': user['username'], 'platform': user.get('platform', 'Unknown')}
                            for user in data if 'username' in user]
                return {'accounts': accounts}, 200
        except (FileNotFoundError, json.JSONDecodeError):
            return {'accounts': []}, 200