import json
import time

import openai
from flask import jsonify
from instabot import Bot

from instagrapi import Client

class InstagramBot:
    def __init__(self, username, password):
        self.client = Client()
        self.client.login(username, password)
        self.log_list = []

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

    def log_and_print(self, message):
        try:
            with open("log_file.txt", "a", encoding="utf-8") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except UnicodeEncodeError:
            # Ignoriere den Fehler und protokolliere die Nachricht ohne Emojis
            cleaned_message = message.encode('ascii', 'ignore').decode('ascii')
            with open("log_file.txt", "a", encoding="utf-8") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {cleaned_message}\n")
        print(message)

    def generate_ki_comment(self):
        # Stelle sicher, dass der API-Key sicher gehandhabt wird
        openai.api_key = "test"

        # Nachrichtenstruktur definieren
        nachrichten = [
            {
                "role": "system",
                "content": "You are an AI specialized in generating engaging and relevant comments for social media posts, particularly for Instagram. You understand "
                           "the nuances of social interaction online and can craft comments that are appropriate for various types of posts, whether they are personal, "
                           "business-related, or for entertainment purposes. Your comments are concise, respectful, and add value to the conversation. Please generate a "
                           "comment suitable for an Instagram post. Do not use emojis in the comment."

            },
            {
                "role": "user",
                "content": "Generate a nice comment for an Instagram post with a maximum of 50 characters. and a minumum of 20"
            }
        ]

        # API-Anfrage
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=nachrichten
            )
            # Extrahiere und gib das Kommentar zurück
            if response.choices and response.choices[0].message:
                kommentar = response.choices[0].message['content']
                if len(kommentar) <= 50:
                    return kommentar
                else:
                    return "Kommentar zu lang (> 50 Zeichen)."
            else:
                return "Keine gültige Antwort erhalten."

        except Exception as e:
            return f"Fehler bei der Kommentargenerierung: {e}"


    def generate_ki_message(self):
        # Stelle sicher, dass der API-Key sicher gehandhabt wird
        openai.api_key = "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"

        # Nachrichtenstruktur definieren
        nachrichten = [
            {
                "role": "system",
                "content": "You are an AI specialized in creating brief, friendly, and engaging messages for social media, suitable for initiating a new connection. "
                           "Your messages should be warm and convey a sense of wanting to get to know the person, like the beginning of a friendly conversation. "
                           "Please generate a short greeting message that is casual and friendly, aiming to spark a friendly connection. Do not use emojis. "
                           "The message should be 1-3 sentences long."
            },
            {
                "role": "user",
                "content": "Create a friendly and engaging direct message suitable for a instagram user."
            }
        ]

        # API-Anfrage
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=nachrichten
            )
            # Extrahiere und gib die Nachricht zurück
            if response.choices and response.choices[0].message:
                return response.choices[0].message['content']
            else:
                return "Keine gültige Antwort erhalten."

        except Exception as e:
            return f"Fehler bei der Nachrichtengenerierung: {e}"




def execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    duration = float(duration)
    follower_count = int(follower_count)
    duration_interaction = duration * 24 * 60 * 60 / follower_count

    bot = InstagramBot(username, password)
    bot.log_and_print("erfolgreich eingeloggt")

    follower_ids = bot.get_followers(target_username, follower_count)
    if not follower_ids:
        bot.log_and_print("Fehler beim Abrufen der Follower oder keine Follower gefunden.")
        return

    for user_id in follower_ids:
        try:
            bot.follow_user(user_id)
            bot.log_and_print(f"Nutzer {user_id} gefolgt")

            last_post_id = bot.get_last_post_of_user(user_id)
            if last_post_id:
                if like_posts:
                    try:
                        bot.like_latest_post(last_post_id)
                        bot.log_and_print(f"Beitrag geliked {last_post_id}")
                    except Exception as e:
                        bot.log_and_print(f"Fehler beim Liken des Beitrags: {e}")

                if comment_on_posts:
                    if comment_method == "manuell":
                        try:
                            bot.comment_post_by_id(last_post_id, comment_input)
                            bot.log_and_print(f"Post kommentiert mit der ID {last_post_id}")
                        except Exception as e:
                            bot.log_and_print(f"Fehler beim Kommentieren: {e}")
                    else:
                        # Verwende den KI-generierten Kommentar
                        try:
                            ki_comment = bot.generate_ki_comment()
                            bot.comment_post_by_id(last_post_id, ki_comment)
                            bot.log_and_print(f"KI-Kommentar gesendet {ki_comment} an Post {last_post_id}")
                        except Exception as e:
                            bot.log_and_print(f"Fehler beim Senden des KI-Kommentars: {e}")

            else:
                bot.log_and_print(f"Keine Beiträge gefunden für Nutzer {user_id}")

        except Exception as e:
            bot.log_and_print(f"Fehler bei Interaktion mit Nutzer {user_id}: {e}")

        if send_message:
            if message_method == "manuell":
                try:
                    bot.send_message_to_user(user_id, message_input)
                    bot.log_and_print(f"Nachricht gesendet an Nutzer {user_id}")
                except Exception as e:
                    bot.log_and_print(f"Fehler beim Senden der Nachricht: {e}")
            else:
                # Verwende die KI-generierte Nachricht
                try:
                    ki_message = bot.generate_ki_message()
                    bot.send_message_to_user(user_id, ki_message)
                    bot.log_and_print(f"KI-Nachricht {ki_message} gesendet an Nutzer {user_id}")
                except Exception as e:
                    bot.log_and_print(f"Fehler beim Senden der KI-Nachricht: {e}")

        time.sleep(duration_interaction)

    return {'status': 'success', 'message': 'Bot-Aktionen ausgeführt'}




def run_bot_in_background(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    try:
        # Hier rufen Sie Ihre Langzeitfunktion auf
        execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input)
        print("Bot-Aktionen abgeschlossen!")
    except Exception as e:
        print(f"Fehler bei der Ausführung des Bots: {e}")



