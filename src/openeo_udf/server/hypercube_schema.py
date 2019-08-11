# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

from openeo_udf.server.dimension_schema import DimensionSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class HyperCubeSchema(Schema):
    description = "A multi dimensional hypercube with configurable dimensions."
    type = "object"
    required = ["id", "data", "dimension"]
    properties = {
        "id": {
            "description": "The identifier of this hyper cube.",
            "type": "string"
        },

        "array": {
            "description": "A multi-dimensional array of integer (8,16,32,64 bit) or float (16, 32, 64 bit) values." \
                           "By default index dimension is as follows: [time][y][x]. Hence, the index data[0] returns " \
                           "the 2D slice for the first time-stamp. The y-indexing if counted from top to bottom " \
                           "and represents the rows of the 2D array. The x-indexing is counted from left to right " \
                           "and represents the columns of the 2D array. The dimension options must be used ot describe "
                           "other dimension configurations.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "float"}
                }
            }
        },
        "dimensions": {
            "description": "The description of each dimension and the value as ordered list. "
                           "The order of the dimension in this array "
                           "is the order of the dimension in the hypercube. The dimension with the name "
                           "*value* described the cell value.",
            "type": "array",
            "items": {
                "type": DimensionSchema
            }
        }
    }
    example = {
        "id": "test_data",
        "data": [
            [
                [0.0, 0.1],
                [0.2, 0.3]
            ],
            [
                [0.0, 0.1],
                [0.2, 0.3]
            ]
        ],
        "dimension": [{"name": "time", "unit": "ISO:8601", "coordinates":["2001-01-01", "2001-01-02"]},
                      {"name": "X", "unit": "degree", "coordinates":[50.0, 60.0]},
                      {"name": "Y", "unit": "degree", "coordinates":[40.0, 50.0]},
                     ]
    }

