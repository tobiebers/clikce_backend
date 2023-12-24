import json
import time

from flask import jsonify
from instabot import Bot

class InstaBot:
    def __init__(self, username, password):
        self.bot = Bot()
        self.username = username
        self.password = password

    def login(self):
        self.bot.login(username=self.username, password=self.password)

    def upload_post(self, image_path, caption):
        self.bot.upload_photo(image_path, caption=caption)

    def get_user_followers(self, user_id, max_count):
        followers = self.bot.get_user_followers(user_id, max_count)
        return followers

    def follow_user(self, user_id):
        self.bot.follow(user_id)

    def get_last_post_of_user(self, user_id):
        media_ids = self.bot.get_user_medias(user_id, filtration=None)
        return media_ids[0] if media_ids else None

    def like_post(self, media_id):
        self.bot.like(media_id)

    def comment_post(self, media_id, comment_text):
        self.bot.comment(media_id, comment_text)

    def send_message(self, user_id, message_text):
        self.bot.send_message(message_text, [user_id])

    def get_user_id(self, username):
        return self.bot.get_user_id_from_username(username)

    def logout(self):
        self.bot.logout()


def execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    # umwandeln in minuten und ausrechnen der zwischenräume
    duration = float(duration)
    print(" Die anzahl der Tage ist", duration)
    follower_count = float(follower_count)
    duration_interaction = duration * 24 * 60 * 60 / follower_count
    print("Es wird immer in", duration_interaction, "eine Aktion suageführt")

    #Bot erstellen und einloggen
    try:
        my_bot = InstaBot(username, password)
        my_bot.login()
    except Exception as e:
        print(f"Fehler beim einloggen: {e}")

    #Liste von Followern von Target holen
    try:
        follower_count = int(follower_count)
    except ValueError:
        print("Follower_count muss eine ganze Zahl sein")
        return

    try:
        followers = my_bot.get_user_followers(target_username, follower_count)
        time.sleep(2)
        print("Die Liste ist", followers)
        if not followers:
            print("Keine Follower gefunden oder Fehler beim Abrufen")
            return
    except Exception as e:
        print(f"Fehler beim Abrufen der Follower des Targets: {e}")
        return
    if not followers:
        print("Keine Follower gefunden")
        return

    time.sleep(5)
    while followers:
        print("Verbleibende Objekte in der Liste:", len(followers))
        #Ersten Namen aus der Liste holen
        user_id = followers[0]
        print("der Nutzername ist", user_id)


        try:
            my_bot.follow_user(user_id)
        except Exception as e:
            print(f"Fehler beim folgen des nutzers: {e}")
            pass


        if like_posts or comment_on_posts:
            try:
                last_post_id = my_bot.get_last_post_of_user(user_id)

                if like_posts:
                    try:
                        my_bot.like_post(last_post_id)
                    except Exception as e:
                        print(f"Fehler beim Liken des Posts: {e}")

                if comment_on_posts:
                    if comment_method == "ki":
                        try:
                            print("Kommentieren mit KI")

                        except Exception as e:
                            print(f"Fehler beim Kommentieren mit KI: {e}")
                    elif comment_method == 'manuel':
                        try:
                            my_bot.comment_post(last_post_id, comment_input)
                        except Exception as e:
                            print(f"Fehler beim manuellen Kommentieren: {e}")
            except Exception as e:
                print(f"Fehler bei Like/Comment Aktionen: {e}")

        if send_message:
            if message_method == "ki":
                try:
                    print("Nachricht senden mit KI")
                    # Hier Code zum Senden von Nachrichten mit KI einfügen
                except Exception as e:
                    print(f"Fehler beim Senden der Nachricht mit KI: {e}")
            elif message_method == 'manuel':
                try:
                    print("Manuelles Nachrichten senden")
                    my_bot.send_message(user_id, message_input)
                except Exception as e:
                    print(f"Fehler beim manuellen Senden der Nachricht: {e}")

        followers.pop(0)
        print("Element aus der liste gelöscht")
        time.sleep(180)

    return {'status': 'success', 'message': 'Bot-Aktionen ausgeführt'}



def run_bot_in_background(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    try:
        # Hier rufen Sie Ihre Langzeitfunktion auf
        execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input)
        print("Bot-Aktionen abgeschlossen!")
    except Exception as e:
        print(f"Fehler bei der Ausführung des Bots: {e}")



