from datetime import timedelta, datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json
import os
import openai
import json

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