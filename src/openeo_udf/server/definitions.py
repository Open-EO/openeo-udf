# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


#####################################################################

class SpatialExtent(Schema):
    description = "spatial extent with resolution information"
    type = "object"
    properties = {
        "north": {
            "description": "The northern border.",
            "type": "float"
        },
        "south": {
            "description": "The southern border.",
            "type": "float"
        },
        "east": {
            "description": "The eastern border.",
            "type": "float"
        },
        "west": {
            "description": "The western border.",
            "type": "float"
        },
        "nsres": {
            "description": "The north-south resolution in projection units.",
            "type": "float"
        },
        "ewres": {
            "description": "The east-west resolution in projection units.",
            "type": "float"
        }
    }
    example = {
        "extent": {
            "north": 53,
            "south": 50,
            "east": 30,
            "west": 24,
            "nsres": 0.01,
            "ewres": 0.01
        }
    }


#####################################################################

class ImageCollectionTile(Schema):
    description = "A three dimensional tile of data that represents a spatio-temporal " \
                  "subset of a spatio-temporal image collection. "
    type = "object"
    required = ["data", "id", "extent"]
    properties = {
        "id": {
            "description": "The identifier of this image collection tile.",
            "type": "string"
        },
        "wavelength": {
            "description": "The wavelength of the image collection tile.",
            "type": "float"
        },
        "data":{
            "description": "A three dimensional array fo integer (8,16,32,64 bit) or float (16, 32, 64 bit) values." \
                           "The index dimension is as follows: [time][y][x]. Hence, the index data[0] returns " \
                           "the 2D slice for the first time-stamp. The y-indexing if counted from top to bottom " \
                           "and represents the rows of the 2D array. The x-indexing is counted from left to right " \
                           "and represents the columns of the 2D array.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "float"
                    }
                }
            }
        },
        "start_times": {
            "description": "The array that contains that start time values for each x,y slice."
                           "As date-time string format ISO 8601 must be supported.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "end_times": {
            "description": "The vector that contains that end time values for each x,y slice, in case the "
                           "the time stamps for all or a subset of slices are intervals. For time instances "
                           "the from and to time stamps must be equal or empty. "
                           "As date-time string format ISO 8601 must "
                           "be supported",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "extent": SpatialExtent
    }
    example = {
        "id": "test_data",
        "wavelength": 420,
        "start_times": ["2001-01-01T00:00:00",
                        "2001-01-02T00:00:00",
                        "2001-01-03T00:00:00"],
        "end_times": ["2001-01-02T00:00:00",
                      "2001-01-03T00:00:00",
                      "2001-01-04T00:00:00"],
        "data": [
            [
                [0, 0, 0],
                [1, 1, 1],
                [2, 2, 2]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [2, 2, 2]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [2, 2, 2]
            ]
        ],
        "extent": {
            "north": 53,
            "south": 50,
            "east": 30,
            "west": 24,
            "nsres": 0.01,
            "ewres": 0.01
        }
    }


#####################################################################

class VectorFeature(Schema):
    description = "A single vector feature with attribute data."
    type = "object"
    required = ["geometry"]
    properties = {
        "geometry": {
            "description": "WKT string of a vector feature of type Point, "
                           "MultiPoint, Line, MultiLine, Polygon or MultiPolygon.",
            "type": "string"
        },
        "attributes": {
            "description": "A list of attributes",
            "type": "array",
            "items": {"type": "string"}
        }
    }
    example = {
        "geometry": "POINT(0, 0)",
        "attributes": ["1", "F"]
    }


#####################################################################

class VectorTile(Schema):
    description = "A tile of vector data that represents a " \
                  "spatio-temporal subset of a spatio-temporal " \
                  "vector dataset. "
    type = "object"
    required = ["data", "column_names", "id", "extent"]
    properties = {
        "id": {
            "description": "The identifier of this vector tile.",
            "type": "string"
        },
        "column_names": {
            "description": "The names of the attribute columns.",
            "type": "array",
            "items": {"type": "string"}
        },
        "data": {
            "description": "The array the vector features including attribute data.",
            "type": "array",
            "items": VectorFeature
        },
        "start_times": {
            "description": "The array that contains that start time values for each vector feature."
                           "As date-time string format ISO 8601 must be supported.",
            "type": "array",
            "items": {"type": "string"}
        },
        "end_times": {
            "description": "The vector that contains that end time values for each vector feature, in case the "
                           "the time stamps for all or a subset of slices are intervals. For time instances "
                           "the from and to time stamps must be equal or empty. "
                           "As date-time string format ISO 8601 must be supported.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "extent": SpatialExtent
    }
    example = {
        "id": "test_data",
        "start_times": ["2001-01-01T00:00:00",
                        "2001-01-02T00:00:00",
                        "2001-01-03T00:00:00"],
        "end_times": ["2001-01-02T00:00:00",
                      "2001-01-03T00:00:00",
                      "2001-01-04T00:00:00"],
        "data": (
            {"geometry": "POINT(30, 53)", "attributes": ["1", "A"]},
            {"geometry": "POINT(24, 50)", "attributes": ["2", "B"]},
            {"geometry": "POINT(27, 52)", "attributes": ["3", "C"]}
        ),
        "column_names": ["id", "format"],
        "extent": {
            "north": 53,
            "south": 50,
            "east": 30,
            "west": 24
        }
    }


#####################################################################

class MachineLearnModel(Schema):
    description = "A machine learn model that should be downloaded and applied to the UDF data."
    type = "object"
    required = ["proj"]
    properties = {
        "framework": {
            "type": "string",
            "description": "The framework that was used to train the model",
            "enum": ["scikit", "pytorch", "tensorflow", "R"]
        },
        "name": {
            "type": "string",
            "description": "The name of the machine learn model."
        },
        "url": {
            "type": "string",
            "description": "The url to the model file."
        }
    }
    example = {"framework": "sckit",
               "name": "random_forest",
               "url": "http://my.model.com/model.p"}


#####################################################################

class UdfData(Schema):
    description = "The UDF data object that stores image collection tiles, vector tiles," \
                  " projection information and machine learn models. This object is argument for the " \
                  "UDF as well as their return value."
    type = "object"
    required = ["proj"]
    properties = {
        "proj": {
            "type": "string",
            "description": "The EPSG code or WKT projection string. eg: EPSG:4326"
        },
        "image_collection_tiles": {
            "description": "A list of image collection tiles. Each tile represents a single "
                           "image band or other scalar values like temperature.",
            "type": "array",
            "items": ImageCollectionTile
        },
        "vector_tiles": {
            "description": "A list of vector tiles.",
            "type": "array",
            "items": VectorTile
        },
        "models": {
            "description": "A list of machine learn models.",
            "type": "array",
            "items": MachineLearnModel
        }
    }
    example = {
        "proj": "EPSG:4326",
        "image_collection_tiles": [
            {
                "id": "test_data",
                "wavelength": 420,
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00",
                                "2001-01-03T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00",
                              "2001-01-04T00:00:00"],
                "data": [
                    [
                        [0, 0, 0],
                        [1, 1, 1],
                        [2, 2, 2]
                    ],
                    [
                        [0, 0, 0],
                        [1, 1, 1],
                        [2, 2, 2]
                    ],
                    [
                        [0, 0, 0],
                        [1, 1, 1],
                        [2, 2, 2]
                    ]
                ],
                "extent": {
                    "north": 53,
                    "south": 50,
                    "east": 30,
                    "west": 24,
                    "nsres": 0.01,
                    "ewres": 0.01
                }
            }
        ],
        "vector_tiles": [
            {
                "id": "test_data",
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00",
                                "2001-01-03T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00",
                              "2001-01-04T00:00:00"],
                "data": (
                    {"geometry": "POINT(30, 53)", "attributes": ["1", "A"]},
                    {"geometry": "POINT(24, 50)", "attributes": ["2", "B"]},
                    {"geometry": "POINT(27, 52)", "attributes": ["3", "C"]}
                ),
                "column_names": ["id", "format"],
                "extent": {
                    "north": 53,
                    "south": 50,
                    "east": 30,
                    "west": 24
                }
            }
        ]
    }


class UdfCode(Schema):
    description = "The object that stores the UDF code and language specification."
    type = "object"
    required = ["language", "code"]
    properties = {
        "language": {
            "type": "string",
            "description": "The language of UDF code"
        },
        "code": {
            "type": "string",
            "description": "The UDF code"
        }
    }
    example = {
        "language": "python",
        "code": "import numpy as np \n"
                " \n"
                "def udf(data): \n"
                "    pass\n"
    }
