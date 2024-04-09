from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from Classes.UserService import UserService
from database_clone import DataBase
from database_clone.DataBase import JsonDatabase
from functions.main_instaloader import InstaloaderClient
import json
db = JsonDatabase('database_clone/UserQuestionsDataBase.json')

class Login(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.json
        result = self.user_service.login(data.get('email'), data.get('password'))
        return result, 200


class SubmitAnswers(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.get_json()
        result = self.user_service.submit_answers(data)
        return result, 200

class ChangeAnswers(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.get_json()
        result = self.user_service.change_answer(data.get('key'), data.get('answer'))
        return result, 200

class SettingProfile(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def post(self):
        data = request.json
        result = self.user_service.update_profile(data.get('firstname'), data.get('lastname'), data.get('branche'), data.get('language'), data.get('password'), data.get('goals'), data.get('description'))
        return result, 200




class FetchAnswers(Resource):
    def __init__(self):
        self.user_service = UserService(db)

    def get(self):
        data = self.user_service.fetch_answers()
        return jsonify(data)



