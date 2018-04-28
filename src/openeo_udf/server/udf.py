# -*- coding: utf-8 -*-
from flask import make_response, jsonify, request
from flask_restful import abort, Resource
from flask_restful_swagger_2 import swagger
from .definitions import UdfData, UdfCode, UdfRequest

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


POST_JOBS_DOC = {
    "description": "Run a Python user defined function (UDF) with data",
    "tags": ["UDF"],
    "parameters": [
        {
            "name": "data",
            "in": "body",
            'required': True,
            "description": "The data for the provided UDF",
            "schema": UdfRequest
        }
    ],
    'consumes':['application/json'],
    'produces':["application/json"],
    "responses": {
        "200": {
            "description": "The result of the UDF computation.",
            "schema": UdfData
        }
    }
}


class Udf(Resource):
    @swagger.doc(POST_JOBS_DOC)
    def post(self):

        if request.is_json is False:
            return False

        request_data = request.get_json()
        print(request_data)

        return make_response(jsonify(UdfData.example), 200)
