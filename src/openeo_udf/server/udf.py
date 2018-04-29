# -*- coding: utf-8 -*-
import traceback
import sys
from flask import make_response, jsonify, request, json
from flask_restful import abort, Resource
from flask_restful_swagger_2 import swagger
from .definitions import UdfData, UdfCode, UdfRequest, ErrorResponse
from ..api.run_code import run_json_user_code

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
            "description": "The UDF source code and data tp process",
            "schema": UdfRequest
        }
    ],
    'consumes':['application/json'],
    'produces':["application/json"],
    "responses": {
        "200": {
            "description": "The result of the UDF computation.",
            "schema": UdfData
        },
        "400": {
            "description": "The error message.",
            "schema": ErrorResponse
        }
    }
}


class Udf(Resource):
    @swagger.doc(POST_JOBS_DOC)
    def post(self):

        try:
            if request.is_json is False:
                raise Exception("Missing JSON in request")

            json_data = request.get_json()
            result = run_json_user_code(json_data=json_data)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponse(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)

        return make_response(jsonify(result), 200)
