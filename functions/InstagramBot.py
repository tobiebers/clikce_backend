import json
import time

from flask import jsonify
from instabot import Bot

from instagrapi import Client

class InstagramBot:
    def __init__(self, username, password):
        self.client = Client()
        self.client.login(username, password)

    def get_followers(self, target_username, follower_count):
        user_id = self.client.user_id_from_username(target_username)
        followers = self.client.user_followers(user_id, amount=follower_count)
        return followers

    def follow_user(self, user_id):
        self.client.user_follow(user_id)

    def get_last_post_of_user(self, user_id):
        user_posts = self.client.user_medias(user_id, amount=1)
        if user_posts:
            return user_posts[0].id
        return None

    def like_latest_post(self, last_post_id):
        self.client.media_like(last_post_id)

    def comment_post_by_id(self, post_id, comment):
        self.client.media_comment(post_id, comment)

    def send_message_to_user(self, user_id, message):
        self.client.direct_send(message, [user_id])




def execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    duration = float(duration)
    follower_count = int(follower_count)
    duration_interaction = duration * 24 * 60 * 60 / follower_count

    # Erstellen einer Instanz von InstagramBot
    bot = InstagramBot(username, password)
    print("erfolgreich eingeloggt")

    follower_ids = bot.get_followers(target_username, follower_count)

    if not follower_ids:
        print("Fehler beim Abrufen der Follower oder keine Follower gefunden.")
        return

    for user_id in follower_ids:
        try:
            bot.follow_user(user_id)
            print("Nutzer", user_id, "gefolgt")

            last_post_id = bot.get_last_post_of_user(user_id)
            if last_post_id:
                if like_posts:
                    try:
                        bot.like_latest_post(last_post_id)
                        print("Beitrag geliked", last_post_id)
                    except Exception as e:
                        print(f"Fehler beim Liken des Beitrags: {e}")

                if comment_on_posts:
                    try:
                        bot.comment_post_by_id(last_post_id, comment_input)
                        print("Post kommentiert mit der ID", last_post_id)
                    except Exception as e:
                        print(f"Fehler beim Kommentieren: {e}")
            else:
                print(f"Keine Beiträge gefunden für Nutzer {user_id}")

        except Exception as e:
            print(f"Fehler bei Interaktion mit Nutzer {user_id}: {e}")

        if send_message:
            try:
                bot.send_message_to_user(user_id, message_input)
                print("Nachricht gesendet an Nutzer", user_id)
            except Exception as e:
                print(f"Fehler beim Senden der Nachricht: {e}")

        time.sleep(duration_interaction)

    return {'status': 'success', 'message': 'Bot-Aktionen ausgeführt'}




def run_bot_in_background(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    try:
        # Hier rufen Sie Ihre Langzeitfunktion auf
        execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input)
        print("Bot-Aktionen abgeschlossen!")
    except Exception as e:
        print(f"Fehler bei der Ausführung des Bots: {e}")



