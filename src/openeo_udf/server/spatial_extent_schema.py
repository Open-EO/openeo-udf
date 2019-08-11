# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class SpatialExtentSchema(Schema):
    description = "spatial extent with resolution information"
    type = "object"
    properties = {
        "top": {
            "description": "The top (north) border.",
            "type": "float"
        },
        "bottom": {
            "description": "The bottom (south) border.",
            "type": "float"
        },
        "right": {
            "description": "The right (eastern) border.",
            "type": "float"
        },
        "left": {
            "description": "The left (wester) border.",
            "type": "float"
        },
        "height": {
            "description": "The top-bottom resolution in projection units.",
            "type": "float"
        },
        "width": {
            "description": "The right-left resolution in projection units.",
            "type": "float"
        }
    }
    example = {
        "extent": {
            "top": 53,
            "bottom": 50,
            "right": 30,
            "left": 24,
            "height": 0.01,
            "width": 0.01
        }
    }

