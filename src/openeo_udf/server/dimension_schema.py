# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DimensionSchema(Schema):
    description = "Description of a single dimension. "
    type = "object"
    required = ["name"]
    properties = {
        "name": {
            "description": "The name of the dimension, like *time*, *X*, *Y*, *Z* and so on.",
            "type": "string"
        },
        "description": {
            "description": "Description of the dimension.",
            "type": "string"
        },
        "unit": {
            "description": "The unit of the dimension. The unit can be *ISO:8601* for time; "
                           "metric length units based on meter: *nm* (nanometer), "
                           "*mm* (millimeter), *cm* (centimeter), "
                           "*m* (meter), *dm* (decimeter), *km* (kilometer); "
                           "temperature *K* (Kelvin), *C* (degree Celsius);"
                           "lat-lon coordinates in *degree*;"
                           "earth observation units: NDVI, DVI, ... ; "
                           "sensor units: *int8*, *int16*, *int32*; "
                           "user defined units: *user_lala* ",
            "type": "string"
        },
        "coordinates": {
            "description": "The array that contains the coordinates of the specific dimension. "
                           "This parameter is optional.",
            "type": "array",
            "items": {"type": "float"}
        },
    }
