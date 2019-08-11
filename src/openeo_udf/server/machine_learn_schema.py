# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class MachineLearnModelSchema(Schema):
    description = "A machine learn model that should be applied to the UDF data."
    type = "object"
    required = ["framework", "path"]
    properties = {
        "framework": {
            "type": "string",
            "description": "The framework that was used to train the model",
            "enum": ["sklearn", "pytorch", "tensorflow", "R"]
        },
        "name": {
            "type": "string",
            "description": "The name of the machine learn model."
        },
        "description": {
            "type": "string",
            "description": "The description of the machine learn model."
        },
        "path": {
            "type": "string",
            "description": "The path to the machine learn model file to which the UDF must have read access."
        },
        "md5_nash": {
            "type": "string",
            "description": "The md5 checksum of the model that should be used to identify "
                           "the machine learn model in the UDF storage system. "
                           "The machine learn model must be uploaded to the UDF server."
        }
    }
    example = {"framework": "sklearn",
               "name": "random_forest",
               "description": "A random forest model",
               "path": "/tmp/model.pkl.xz"}
