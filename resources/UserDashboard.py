from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from database_clone import DataBase
from database_clone.DataBase import JsonDatabase

db = JsonDatabase('database_clone/UserQuestionsDataBase.json')

class FetchChart(Resource):
    def get(self):
        # Annahme: Du speicherst den Text für Abschnitt 1 im Backend


        visitors1_text = 40
        visitors2_text = 80
        visitors3_text = 20
        visitors4_text = 40
        visitors5_text = 60
        visitors6_text = 0
        visitors7_text = 100
        visitors8_text = 20
        visitors9_text = 60
        visitors10_text = 40




        return jsonify({
            'visitors1': visitors1_text,
            'visitors2': visitors2_text,
            'visitors3': visitors3_text,
            'visitors4': visitors4_text,
            'visitors5': visitors5_text,
            'visitors6': visitors6_text,
            'visitors7': visitors7_text,
            'visitors8': visitors8_text,
            'visitors9': visitors9_text,
            'visitors10': visitors10_text,

        })