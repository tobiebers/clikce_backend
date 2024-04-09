import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
from Classes.CalendarService import CalendarService



class PostInstagramMedia(Resource):
    def __init__(self):
        self.service = CalendarService()

    def post(self):
        uploaded_file = request.files['file']
        caption = request.form['caption']
        accounts = json.loads(request.form['accounts'])
        return self.service.post_instagram_media(uploaded_file, caption, accounts)



class PlannedPosts(Resource):
    def __init__(self):
        self.service = CalendarService()

    def get(self):
        return self.service.get_planned_posts()


class PlanPost(Resource):
    def __init__(self):
        self.service = CalendarService()

    def post(self):
        if 'file' not in request.files:
            return {'error': 'Keine Datei hochgeladen'}, 400

        uploaded_file = request.files['file']
        date = request.form.get('date')
        time = request.form.get('time')
        account = request.form.get('accounts')
        caption = request.form.get('caption')

        return self.service.plan_post(uploaded_file, date, time, account, caption)


class CreateHashtagSet(Resource):
    def __init__(self):
        self.service = CalendarService()

    def post(self):
        data = request.get_json()
        return jsonify(self.service.create_hashtag_set(data.get('name'), data.get('hashtags')))

class GetHashtagSets(Resource):
    def __init__(self):
        self.service = CalendarService()

    def get(self):
        return jsonify(self.service.get_hashtag_sets())

