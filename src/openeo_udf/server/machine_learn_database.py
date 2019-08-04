# -*- coding: utf-8 -*-
import traceback
import sys
from flask import make_response, jsonify, request, json
from flask_restful import abort, Resource
from flask_restful_swagger_2 import swagger


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class MachineLearnDatabase(Resource):
    """The machine learn model storage"""

    def get(self, md5_hash: str):
        return make_response(jsonify(md5_hash), 200)

    def delete(self, md5_hash: str):
        return make_response(jsonify(md5_hash), 200)

    def post(self, url: str):
        return make_response(jsonify(url), 200)