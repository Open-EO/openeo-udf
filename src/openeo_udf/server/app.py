# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"

flask_app = Flask(__name__)
CORS(flask_app)

flask_api = Api(flask_app,
                api_version='0.1pre-alpha',
                api_spec_url='/api/v0/swagger',
                title="OpenEO UDF API",
                description="The OpenEO UDF API specification",
                schemes=['http', 'https'],
                consumes=['application/json'])

flask_api._swagger_object["securityDefinitions"] = {"basicAuth": {"type": "basic"}}
flask_api._swagger_object["security"] = [{"basicAuth": []}]
flask_api._swagger_object["tags"] = [
    {
        "name": "UDF",
        "description": "Interfacing end executing user-defined functions at the provided data."
    }
]

flask_api._swagger_object["responses"] = {
    "auth_required": {
        "description": "The back-end requires clients to authenticate in order to process this request."
    },
    "not_implemented": {
        "description": "This API feature is not supported by the back-end."
    },
    "access_denied": {
        "description": "Authorization failed, access to the requested resource has been denied."
    },
    "unavailable": {
        "description": "The service is currently unavailable."
    }
}
