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
    "description": "Run a Python user defined function (UDF) on the provided data",
    "tags": ["UDF"],
    "parameters": [
        {
            "name": "data",
            "in": "body",
            'required': True,
            "description": "The UDF Python source code and data as JSON definition to process",
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
        """Execute the UDF code

        TODO: Improve this method with with support for binary serialization

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

        >>> d = dict(array=[1,2,3,4,5], name="Test", meta=dict(a="a", b=2))
        >>> msgpack.packb(d)
        b'\x83\xa5array\x95\x01\x02\x03\x04\x05\xa4name\xa4Test\xa4meta\x82\xa1a\xa1a\xa1b\x02'
        >>> msgpack.unpackb(_)
        {b'array': [1, 2, 3, 4, 5], b'name': b'Test', b'meta': {b'a': b'a', b'b': 2}}

        """

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
