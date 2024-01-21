import json
import time

from flask import jsonify
from instabot import Bot

from instagrapi import Client






def follow_user(client, user_id):
    # Folge dem Nutzer
    client.user_follow(user_id)


def get_last_post_of_user(client, user_id):
    # Abrufen des neuesten Beitrags des Benutzers
    user_posts = client.user_medias(user_id, amount=1)  # amount=1 um nur den neuesten Beitrag zu bekommen
    if user_posts:
        # Rückgabe der ID des neuesten Beitrags
        return user_posts[0].id  # Gibt die ID des neuesten Beitrags zurück
    return None  # Gibt None zurück, wenn der Benutzer keine Beiträge hat




def like_latest_post(client, last_post_id):
    client.media_like(last_post_id)


def comment_post_by_id(client, post_id, comment):
    # Kommentiere den Beitrag mit der gegebenen Post ID
    client.media_comment(post_id, comment)


def send_message_to_user(client, user_id, message):
    # Sende eine Nachricht
    client.direct_send(message, [user_id])

def get_followers(client, target_username, limit):
    # Finde die User ID des Zielnutzers
    user_id = client.user_id_from_username(target_username)
    # Abrufen der Follower
    followers = client.user_followers(user_id, amount=limit)
    return followers





def execute_bot_actions(username, password, duration, follower_count, target_username, like_posts, comment_on_posts, comment_method, comment_input, send_message, message_method, message_input):
    duration = float(duration)
    follower_count = float(follower_count)
    duration_interaction = duration * 24 * 60 * 60 / follower_count

    client = Client()
    client.login(username, password)

    time.sleep(5)

    try:
        followers = get_followers(client, target_username, follower_count)
        follower_ids = list(followers.keys())

        if not follower_ids:
            print("Keine Follower gefunden oder Fehler beim Abrufen")
            return
    except Exception as e:
        print(f"Fehler beim Abrufen der Follower des Targets: {e}")
        return

    for user_id in follower_ids:
        try:
            follow_user(client, user_id)
            print("Nutzer", user_id, "gefolgt")
        except Exception as e:
            print(f"Fehler beim Interagieren mit Nutzer {user_id}: {e}")
            continue

        try:
            last_post_id = get_last_post_of_user(client, user_id)
            if last_post_id:
                if like_posts:
                    try:
                        like_latest_post(client, last_post_id)
                        print("Beitrag geliked", last_post_id)
                    except Exception as e:
                        print(f"Fehler beim Liken des Beitrags: {e}")

                if comment_on_posts:
                    try:
                        comment_post_by_id(client, last_post_id, comment_input)
                        print("Post kommentiert mit der ID", last_post_id)
                    except Exception as e:
                        print(f"Fehler beim Kommentieren: {e}")
            else:
                print(f"Keine Beiträge gefunden für Nutzer {user_id}")
        except Exception as e:
            print(f"Fehler bei Like/Comment Aktionen: {e}")

        if send_message:
            try:
                send_message_to_user(client, user_id, message_input)
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



