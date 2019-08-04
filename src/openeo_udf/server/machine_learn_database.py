# -*- coding: utf-8 -*-
import traceback
import sys
import os
from shutil import copyfile
from hashlib import md5
from os import listdir
from os.path import isfile, join
from flask import make_response, jsonify, request, json
from flask_restful import abort, Resource
from openeo_udf.server.definitions import ErrorResponse
from openeo_udf.server.config import UdfConfiguration


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"



class MachineLearnDatabase(Resource):
    """The machine learn model storage"""

    def get(self):
        """Return all md5 hashes of the stored machine learn models as list
        """
        try:
            path = UdfConfiguration.machine_learn_storage_path
            if os.path.isdir(path):
                hash_list = [f for f in listdir(path) if isfile(join(path, f))]
                return make_response(jsonify(hash_list), 200)

            response = ErrorResponse(message=f"The storage path of the machine learn models was not found on server.")
            return make_response(jsonify(response), 400)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponse(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)

    def delete(self, md5_hash: str):
        """Remove a single machine learn model from the server"""

        try:
            path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)
            if os.path.exists(path):
                os.remove(path)
                return make_response(jsonify(md5_hash), 200)

            response = ErrorResponse(message=f"The machine learn model for hash {md5_hash} was not found")
            return make_response(jsonify(response), 400)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponse(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)

    def post(self, url: str):

        try:
            if os.path.exists(url):
                path = url
            else:
                # Download the file from the provided url
                pass

            if os.path.exists(path) and os.path.isfile(path):

                md5_hash = md5(open(path, "rb").read()).hexdigest()
                md5_hash_path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)
                copyfile(path, md5_hash_path)

                return make_response(jsonify(md5_hash), 200)

            response = ErrorResponse(message=f"Unable to access machine learn model at {url}")
            return make_response(jsonify(response), 400)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponse(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)
