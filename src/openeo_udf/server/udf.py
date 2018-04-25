# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import abort, Resource
from flask_restful_swagger_2 import swagger
from .definitions import UdfData, UdfCode

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
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
            "schema": UdfData
        },
        {
            "name": "code",
            "in": "body",
            'required': True,
            "description": "The code of the UDF",
            "schema": UdfCode
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
    def post(self, ):
        return make_response(jsonify(UdfData.example), 200)
