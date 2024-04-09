from flask import jsonify
from flask_restful import Resource

from database_clone.DataBase import JsonDatabase

#from ratelimit import limits, sleep_and_retry

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






