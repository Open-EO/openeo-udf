# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

from openeo_udf.server.spatial_extent_schema import SpatialExtentSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class RasterCollectionTileSchema(Schema):
    description = "A three dimensional tile of data that represents a spatio-temporal " \
                  "subset of a spatio-temporal raster collection. "
    type = "object"
    required = ["data", "id", "extent"]
    properties = {
        "id": {
            "description": "The identifier of this raster collection tile.",
            "type": "string"
        },
        "wavelength": {
            "description": "The wavelength of the raster collection tile.",
            "type": "float"
        },
        "data": {

            "description": "A three dimensional array of integer (8,16,32,64 bit) or float (16, 32, 64 bit) values." \
                           "The index dimension is as follows: [time][y][x]. Hence, the index data[0] returns " \
                           "the 2D slice for the first time-stamp. The y-indexing if counted from top to bottom " \
                           "and represents the rows of the 2D array. The x-indexing is counted from left to right " \
                           "and represents the columns of the 2D array.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "float"}
                }
            }
        },
        "start_times": {
            "description": "The array that contains that start time values for each x,y slice."
                           "As date-time string format ISO 8601 must be supported.",
            "type": "array",
            "items": {"type": "string"}
        },
        "end_times": {
            "description": "The vector that contains that end time values for each x,y slice, in case the "
                           "the time stamps for all or a subset of slices are intervals. For time instances "
                           "the from and to time stamps must be equal or empty. "
                           "As date-time string format ISO 8601 must "
                           "be supported",
            "type": "array",
            "items": {"type": "string"}
        },
        "extent": SpatialExtentSchema
    }
    example = {
        "id": "test_data",
        "wavelength": 420,
        "start_times": ["2001-01-01T00:00:00",
                        "2001-01-02T00:00:00"],
        "end_times": ["2001-01-02T00:00:00",
                      "2001-01-03T00:00:00"],
        "data": [
            [
                [0, 1],
                [2, 3]
            ],
            [
                [0, 1],
                [2, 3]
            ]
        ],
        "extent": {
            "top": 53,
            "bottom": 51,
            "right": 30,
            "left": 28,
            "height": 1,
            "width": 1
        }
    }

