from datetime import timedelta, datetime
import threading


from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json
import os
import openai
import json

from functions.InstagramBot import  execute_bot_actions, run_bot_in_background


class CreateCaption(Resource):
    def post(self):
        data = request.get_json()
        caption = data.get('caption')



        openai.api_key = "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"

        # Informationen über Ihr Unternehmen
        info = "Ich bin Influencer"
        language = "deutsch"


        # Erstellen Sie eine Nachrichtenstruktur, um den Kontext und die Anfrage zu definieren
        nachrichten = [
            {
                "role": "system",
                "content": "You are an AI capable of generating social media content, including posts, captions, and relevant hashtags. You have expertise in understanding different types of businesses and their specific needs on social media."
            },
            {
                "role": "user",
                "content": f"{info} "
                           f"Schreibe mir im JSON Format die Antwort in der Sprache {language}. "
                           f"eine Beschreibung für den Post {caption} mit maximal 250 Zeichen mit dem Schlüssel 'caption', "
                           f"und maximal 8 Hashtags mit 50 Zeichen, benutze eine Liste mit dem Schlüssel 'hashtags'."
            }
        ]

        # API-Anfrage
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=nachrichten
        )

        # Antwort ausgeben und als JSON parsen
        antwort_json = response.choices[0].message['content']

        # Versuch, die Antwort als JSON zu parsen
        try:
            antwort_dict = json.loads(antwort_json)
            caption = antwort_dict.get('caption', 'Nicht gefunden')
            hashtags = antwort_dict.get('hashtags', 'Nicht gefunden')
            return {'caption': caption, 'hashtags': hashtags}, 200
        except json.JSONDecodeError:
            print("Die Antwort war nicht im gültigen JSON-Format. Antwortinhalt:")
            print(antwort_json)
            return {'error': 'Invalid response format'}, 400


class ScheduleBulkPosts(Resource):
    def post(self):
        file_path = 'database_clone/planned_posts.json'
        schedule_info = request.form

        start_date = datetime.fromisoformat(schedule_info['startDate'])
        post_times = json.loads(schedule_info['postTimes'])
        accounts = json.loads(schedule_info['accounts'])

        uploaded_files = request.files.getlist('files')

        posts = []
        for index, uploaded_file in enumerate(uploaded_files):
            save_path = os.path.join('static', uploaded_file.filename)
            uploaded_file.save(save_path)

            # Ersetzen von Backslashes durch Vorwärtsslashes
            save_path = '/' + save_path.replace('\\', '/')

            post_date = (start_date + timedelta(days=index // len(post_times))).strftime('%Y-%m-%d')
            post_time = post_times[index % len(post_times)]

            posts.append({
                'date': post_date,
                'time': post_time,
                'account': accounts,
                'caption': 'Automatisch generierter Post',
                'picture': save_path
            })

        try:
            if os.path.isfile(file_path):
                with open(file_path, 'r+') as file:
                    existing_posts = json.load(file)
                    existing_posts.extend(posts)
                    file.seek(0)
                    json.dump(existing_posts, file, indent=4)
                    file.truncate()
            else:
                with open(file_path, 'w') as file:
                    json.dump(posts, file, indent=4)

            return {'status': 'success'}, 200
        except Exception as e:
            return {'error': str(e)}, 500




class CreateBot(Resource):
    def post(self):
        data = request.get_json()

        # Debug: Ausgabe der empfangenen Daten
        print("Empfangene Daten:", data)

        # Account-Daten und weitere Parameter extrahieren
        selected_account = data.get('selectedUsernames', [])[0]
        follower_count = data.get('followerCount')
        target_username = data.get('targetUsername')
        duration = data.get('duration')
        like_posts = data.get('likePosts')
        comment_on_posts = data.get('commentOnPosts')
        comment_method = data.get('commentMethod')
        comment_input = data.get('commentInput')
        send_message = data.get('sendMessage')
        message_method = data.get('messageMethod')
        message_input = data.get('messageInput')

        # Debug: Ausgabe der extrahierten Parameter
        print("Selected Account:", selected_account)
        print("Follower Count:", follower_count)
        print("Target Username:", target_username)
        print("Duration:", duration)
        print("Like Posts:", like_posts)
        print("Comment on Posts:", comment_on_posts)
        print("Comment Method:", comment_method)
        print("Comment Input:", comment_input)
        print("Send Message:", send_message)
        print("Message Method:", message_method)
        print("Message Input:", message_input)

        # Account-Daten extrahieren (nehmen Sie das erste ausgewählte Konto)
        selected_account = data.get('selectedUsernames', [])[0]

        # Extrahieren der weiteren Daten
        follower_count = data.get('followerCount')
        target_username = data.get('targetUsername')
        duration = data.get('duration')
        like_posts = data.get('likePosts')
        comment_on_posts = data.get('commentOnPosts')
        comment_method = data.get('commentMethod')
        comment_input = data.get('commentInput')
        send_message = data.get('sendMessage')
        message_method = data.get('messageMethod')
        message_input = data.get('messageInput')

        duration=int(duration)
        follower_count=int(follower_count)

        # Stellen Sie sicher, dass selected_account ein Dictionary ist und einen Benutzernamen enthält
        if isinstance(selected_account, dict) and 'username' in selected_account:
            selected_username = selected_account['username']
        else:
            print("Ungültige Account-Daten:", selected_account)
            return jsonify({'status': 'error', 'message': 'Ungültige Account-Daten'})

        # Lesen des JSON-Files
        try:
            with open('database_clone/instagram_data.json', 'r') as file:
                accounts_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Fehler beim Lesen der Daten: {e}")
            return jsonify({'status': 'error', 'message': 'Fehler beim Lesen der Daten'})

        # Account im JSON-File suchen
        account_info = next((acc for acc in accounts_data if acc['username'] == selected_username), None)

        if account_info:
            print(f"Account gefunden: {account_info}")

            if not account_info.get('bot'):
                # Username und Passwort extrahieren
                username = account_info['username']
                password = account_info['password']
                print(f"Account ist bereit für den Bot. Username: {username}, Password: {password}")

                bot_thread = threading.Thread(target=run_bot_in_background, args=(
                username, password, duration, follower_count, target_username, like_posts, comment_on_posts,
                comment_method, comment_input, send_message, message_method, message_input))
                bot_thread.start()

        return jsonify({'status': 'success', 'message': 'Bot-Daten empfangen und Account validiert'})












