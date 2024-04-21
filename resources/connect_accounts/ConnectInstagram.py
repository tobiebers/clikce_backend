import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import json
import glob
from instabot import Bot

from Classes.InstagramAccountService import InstagramAccountService
from functions.post_schedule import get_credentials, get_image_path, load_user_data

from functions.main_instaloader import InstaloaderClient


class AccountDetails(Resource):
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def get(self):
        return self.service.get_accounts()


class AddInstagramData(Resource):
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def post(self):
        new_data = request.get_json()
        print("Empfangene Daten:", new_data)  # Debug-Print der empfangenen Daten
        result = self.service.add_account(new_data)
        return {'status': 'success'}, 200

class DeleteAccount(Resource):
    def __init__(self):
        self.service = InstagramAccountService('database_clone/instagram_data.json')

    def post(self):
        username = request.get_json().get('username')
        return self.service.delete_account(username)


class FollowerCount(Resource):
    def get(self, username):
        client = InstaloaderClient()
        profile = client.get_profile(username)
        followers = client.get_profile_followers(profile)
        return {'followers': followers}






