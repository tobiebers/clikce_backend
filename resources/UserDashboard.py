from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from database_clone import DataBase
from database_clone.DataBase import JsonDatabase

db = JsonDatabase('database_clone/UserQuestionsDataBase.json')

class FetchChart(Resource):
    def get(self):
        # Annahme: Du hast bereits das Dictionary erstellt
        datensatz = {
            'visitors1': 40,
            'visitors2': 80,
            'visitors3': 20,
            'visitors4': 40,
            'visitors5': 60,
            'visitors6': 0,
            'visitors7': 100,
            'visitors8': 20,
            'visitors9': 60,
            'visitors10': 40
        }

        # Verwende jsonify, um das Dictionary als JSON zu formatieren und zurückzugeben
        return jsonify(datensatz)


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