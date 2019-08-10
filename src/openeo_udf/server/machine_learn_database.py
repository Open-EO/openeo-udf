# -*- coding: utf-8 -*-
import traceback
import sys
import os
from shutil import copyfile
from hashlib import md5
from os import listdir
from os.path import isfile, join
from typing import Optional

import requests
from flask import make_response, jsonify, request
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

    def delete(self):
        """Remove a single machine learn model from the server"""
        md5_hash = str(request.data.decode('ascii'))
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

    def post(self):

        try:
            url = str(request.data.decode('ascii'))
            if os.path.exists(url):
                filepath = url
            else:
                # Check if thr URL exists by investigating the HTTP header
                resp = requests.head(url, allow_redirects=True)

                if resp.status_code != 200:
                    raise Exception("The URL <%s> can not be accessed." % url)

                filename = url.rsplit('/', 1)[1]
                filepath = os.path.join(UdfConfiguration.temporary_storage_path, filename)
                r = requests.get(url, allow_redirects=True)
                open(filepath, 'wb').write(r.content)

            md5_hash = self._compute_md5_hash(filepath)
            if md5_hash:
                return make_response(jsonify(md5_hash), 200)

            response = ErrorResponse(message=f"Unable to access machine learn model at {url}")
            return make_response(jsonify(response), 400)
        except Exception:
            e_type, e_value, e_tb = sys.exc_info()
            response = ErrorResponse(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
            return make_response(jsonify(response), 400)

    @staticmethod
    def _compute_md5_hash(filepath: str) -> Optional[str]:

        if os.path.exists(filepath) and os.path.isfile(filepath):
            md5_hash = md5(open(filepath, "rb").read()).hexdigest()
            md5_hash_path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)
            copyfile(filepath, md5_hash_path)
            return md5_hash
        return None
