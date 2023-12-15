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


from flask import jsonify

class FetchRecentInteractions(Resource):
    def get(self):
        try:
            # Define dropdown options
            account_options = ['Insta', 'Facebook', 'YouTube']
            account_group_options = ['Group 1', 'Group 2', 'Group 3']
            interaction_options = ['Likes', 'Followers', 'Views']

            # Logic to retrieve or calculate data based on selected values
            # ...

            # Construct response data
            data = {
                "account": account_options,
                "account_group": account_group_options,
                "interaction": interaction_options,
                # Include other data as needed
            }

            return jsonify(data)

        except Exception as e:
            return jsonify({"error": str(e)})



class FetchPerformingAccounts(Resource):
    def get(self):
        nameText = "Daviidoji"
        likesText = "176"

        return ({
            'nameText': nameText,
            'likesText': likesText
        })