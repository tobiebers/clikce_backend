from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from ratelimit import sleep_and_retry, limits

from database_clone import DataBase
from database_clone.DataBase import JsonDatabase
import json

from functions.main_instagrabi import InstagrabiClient
#from ratelimit import limits, sleep_and_retry
from functions.main_instaloader import InstaloaderClient

db = JsonDatabase('database_clone/UserQuestionsDataBase.json')




class FetchChartPie(Resource):
    def get(self):
        # Annahme: Du speicherst den Text für Abschnitt 1 im Backend


        datensatz = {
            'Instagram': 40,
            'Facebook': 30,
            'TikTok': 20,
            'YouTube': 40,
        }


        return jsonify(datensatz)






