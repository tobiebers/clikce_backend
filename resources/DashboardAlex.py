from flask import request, jsonify
from flask_restful import Resource
from Classes.Dashboard_Class import Dashboard

dashboard = Dashboard()

class FetchRefreshData(Resource):
    def get(self):
        try:
            success = dashboard.collect_and_store_instagram_data()
            if success:
                return {'message': 'Daten erfolgreich aktualisiert'}, 200
            else:
                return {'message': 'Fehler beim Aktualisieren der Daten'}, 500
        except Exception as e:
            return {'message': str(e)}, 500

class FetchCardInfo(Resource):
    def get(self):
        try:
            data = dashboard.get_card_info()
            return jsonify(data)
        except Exception as e:
            return {'message': str(e)}, 500

class FetchPerformingAccounts(Resource):
    def get(self):
        try:
            data = dashboard.get_performing_accounts_info()
            return jsonify(data)
        except Exception as e:
            return {'message': str(e)}, 500

class FetchChart(Resource):
    def get(self):
        try:
            data = dashboard.get_chart_data()
            return jsonify(data)
        except Exception as e:
            return {'message': str(e)}, 500


class FetchRecentInteractions(Resource):
    def get(self):
        try:
            data = dashboard.get_recent_interactions_data()
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})


class FetchRecentInteractionButton(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            account = json_data['account']
            account_group = json_data['accountGroup']
            interaction = json_data['interaction']

            interaction_count = dashboard.find_interaction_data(account, account_group, interaction.lower())
            return jsonify({'interaction_count': interaction_count})
        except Exception as e:
            return jsonify({'error': str(e)}), 400



