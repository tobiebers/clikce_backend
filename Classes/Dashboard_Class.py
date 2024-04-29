import json
from datetime import datetime
from Classes.Instagrapi_service import InstagrabiClient
from ratelimit import limits, sleep_and_retry

class Dashboard:
    def __init__(self):
        self.json_input_file_path = 'database_clone/instagram_data.json'
        self.json_output_file_path = 'database_clone/alex_data.json'
        self.json_chart_output_file_path = 'database_clone/chart_dashboard.json'

    @sleep_and_retry
    @limits(calls=10, period=3600)
    def collect_and_store_instagram_data(self):
        try:
            with open(self.json_input_file_path, 'r') as file:
                users = json.load(file)

            collected_data = []
            total_likes = 0
            today = datetime.now().strftime('%d-%m')

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

            with open(self.json_output_file_path, 'w') as file:
                json.dump(collected_data, file)

            try:
                with open(self.json_chart_output_file_path, 'r') as file:
                    existing_chart_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_chart_data = []

            chart_data = {"date": today, "total_likes": total_likes}
            existing_chart_data.append(chart_data)

            with open(self.json_chart_output_file_path, 'w') as file:
                json.dump(existing_chart_data, file)

            return True  # Erfolgreich aktualisiert
        except Exception as e:
            raise RuntimeError(f"Fehler beim Aktualisieren der Daten: {str(e)}")

    def get_card_info(self):
        try:
            with open(self.json_output_file_path, 'r') as file:
                data = json.load(file)

            total_likes = sum(user_data['likes'] for user_data in data)
            total_followers = sum(user_data['followers'] for user_data in data)
            total_comments = sum(user_data['comments'] for user_data in data)
            total_followings = sum(user_data['followings'] for user_data in data)

            return {
                'likesText': str(total_likes),
                'followerText': str(total_followers),
                'kommentarText': str(total_comments),
                'followingText': str(total_followings)
            }
        except Exception as e:
            raise RuntimeError(f"Fehler beim Lesen der Karteninformationen: {str(e)}")

    def get_performing_accounts_info(self):
        try:
            with open(self.json_output_file_path, 'r') as file:
                users = json.load(file)

            max_likes = 0
            max_likes_username = ''

            for user in users:
                likes = user['likes']
                if likes > max_likes:
                    max_likes = likes
                    max_likes_username = user['username']

            return {
                'nameText': "Name: " + max_likes_username,
                'likesText': "Likes: " + str(max_likes),
            }
        except Exception as e:
            raise RuntimeError(f"Fehler beim Lesen der Top-Performing-Accounts: {str(e)}")

    def get_chart_data(self):
        try:
            with open(self.json_chart_output_file_path, 'r') as file:
                data = json.load(file)

            # Nehmen Sie die letzten 10 Einträge, falls mehr vorhanden sind
            data = data[-10:]

            return data
        except Exception as e:
            raise RuntimeError(f"Fehler beim Lesen der Chart-Daten: {str(e)}")


    def get_recent_interactions_data(self):
        try:
            with open(self.json_output_file_path, 'r') as file:
                json_data = json.load(file)

            platforms = {entry["platform"] for entry in json_data}
            account_groups = {entry["username"] for entry in json_data}

            account_options = list(platforms)
            account_group_options = list(account_groups)
            interaction_options = ['Likes', 'Followers', 'Followings', 'Comments']

            data = {
                "account": account_options,
                "account_group": account_group_options,
                "interaction": interaction_options,
                # Weitere Daten nach Bedarf einfügen!
            }

            return data
        except Exception as e:
            raise RuntimeError(f"Fehler beim Abrufen der Interaktionsdaten: {str(e)}")

    def find_interaction_data(self, account, account_group, interaction):
        try:
            with open(self.json_output_file_path, 'r') as file:
                json_data = json.load(file)

            for entry in json_data:
                if entry['username'] == account_group and entry['platform'].lower() == account.lower():
                    print("Entry found:", entry)
                    interaction_count = entry.get(interaction.lower(), "Keine Daten gefunden")
                    return interaction_count

            return "Keine Daten gefunden für Account: {} in Plattform: {}".format(account_group, account)
        except Exception as e:
            raise RuntimeError(f"Fehler beim Suchen der Interaktionsdaten: {str(e)}")