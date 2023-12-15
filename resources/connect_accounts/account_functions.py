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

