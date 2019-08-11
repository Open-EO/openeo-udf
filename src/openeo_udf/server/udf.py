# -*- coding: utf-8 -*-
import traceback
import sys
import msgpack
import base64
from flask import make_response, jsonify, request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from openeo_udf.server.udf_schemas import UdfDataSchema, UdfRequestSchema, ErrorResponseSchema
from openeo_udf.api.run_code import run_json_user_code

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

"""
There are several different approached available in python that can be implemented:
- UBJSON https://en.wikipedia.org/wiki/UBJSON
- BSON https://en.wikipedia.org/wiki/BSON
- MessagePack https://en.wikipedia.org/wiki/MessagePack

Important is the support for arrays with integer and floating point numbers that are used in
xarray and numpy. Support for timestamps is required as well. For structured data is the support of lists
and maps important.

              array integer float map time

MessagePack     y      y      y    y    y
BJSON           y      y      y    y    n
UBJSON          n      y      y    n    n

Based on these requirement it seems that MessagePack is the most potent candidate to use
for serialization and supports many different languages.
MessagePack is available here: https://msgpack.org/

Using Messagepack is quite easy:

In [1]: import msgpack
In [2]: import base64
In [3]: d = {1:[1,2,3,4,5,6], "w":"fffff", "d":{"d":"d"}}
In [4]: d
Out[4]: {1: [1, 2, 3, 4, 5, 6], 'w': 'fffff', 'd': {'d': 'd'}}
In [5]: msgpack.packb(d)
Out[5]: b'\x83\x01\x96\x01\x02\x03\x04\x05\x06\xa1w\xa5fffff\xa1d\x81\xa1d\xa1d'
In [6]: p = msgpack.packb(d)
In [7]: base64.b64encode(p)
Out[7]: b'gwGWAQIDBAUGoXelZmZmZmahZIGhZKFk'
In [8]: t = base64.b64encode(p)
In [9]: base64.b64decode(t)
Out[9]: b'\x83\x01\x96\x01\x02\x03\x04\x05\x06\xa1w\xa5fffff\xa1d\x81\xa1d\xa1d'
In [10]: msgpack.unpackb(base64.b64decode(t))
Out[10]: {1: [1, 2, 3, 4, 5, 6], b'w': b'fffff', b'd': {b'd': b'd'}}

"""


POST_JOBS_DOC_UDF = {
    "description": "Run a Python user defined function (UDF) on the provided data",
    "tags": ["UDF"],
    "parameters": [
        {
            "name": "data",
            "in": "body",
            'required': True,
            "description": "The UDF Python source code and data as JSON definition to process",
            "schema": UdfRequestSchema
        }
    ],
    'consumes':['application/json'],
    'produces':["application/json"],
    "responses": {
        "200": {
            "description": "The result of the UDF computation.",
            "schema": UdfDataSchema
        },
        "400": {
            "description": "The error message.",
            "schema": ErrorResponseSchema
        }
    }
}


class Udf(Resource):
    @swagger.doc(POST_JOBS_DOC_UDF)
    def post(self):
        """Execute the UDF code

        """

        try:
            if request.is_json is False:
                raise Exception("Missing JSON in request")

            json_data = request.get_json()
            result = run_json_user_code(dict_data=json_data)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponseSchema(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)

        return make_response(jsonify(result), 200)


POST_JOBS_DOC_UDF_MESSAGE_PACK = {
    "description": "Run a Python user defined function (UDF) on the provided data that are base64 encoded message pack"
                   "binary data",
    "tags": ["UDF"],
    "parameters": [
        {
            "name": "data",
            "in": "body",
            'required': True,
            "description": "The UDF Python source code and data as base64 encoded message pack",
            "schema": UdfRequestSchema
        }
    ],
    'consumes':['application/base64'],
    'produces':["application/base64"],
    "responses": {
        "200": {
            "description": "The result of the UDF computation as base64 encoded message pack.",
            "schema": UdfDataSchema
        },
        "400": {
            "description": "The error message.",
            "schema": ErrorResponseSchema
        }
    }
}


class UdfMessagePack(Resource):
    @swagger.doc(POST_JOBS_DOC_UDF_MESSAGE_PACK)
    def post(self):
        """Execute the UDF code that is encoded as base64 message pack binary format
        """

        try:
            if request.is_json is True:
                raise Exception("JSON is not supported in request. A base64 encoded message pack blob is required.")

            blob = base64.b64decode(request.data)
            dict_data = msgpack.unpackb(blob, raw=False)
            result = run_json_user_code(dict_data=dict_data)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponseSchema(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)

        result = base64.b64encode(msgpack.packb(result))
        return make_response(result, 200)
