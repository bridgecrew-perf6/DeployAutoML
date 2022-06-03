# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 21:52:57 2020

@author: rufus
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from automl import AutoML
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

class Optimize(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        path_to_data = posted_data['path_to_data']
        target_column = posted_data['target_column']
        try: metric = posted_data['metric']
        except KeyError: metric = 'Accuracy'
        auto_ml = AutoML(path_to_data=path_to_data, target_column=target_column, metric=metric)
        try:
            auto_ml.fit()
            return jsonify({ 'Message': 'Success', 'BestModel': str(auto_ml.best_model) })
        except Exception as e:
            return jsonify({ 'Message': str(e) })

api.add_resource(Optimize, '/optimize')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
    
    #python app.py