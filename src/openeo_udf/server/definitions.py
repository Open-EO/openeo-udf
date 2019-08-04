# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


#####################################################################

class SpatialExtent(Schema):
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


#####################################################################

class RasterCollectionTile(Schema):
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
        "extent": SpatialExtent
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


#####################################################################

class Dimension(Schema):
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


#####################################################################

class HyperCube(Schema):
    # TODO: Adjust to xarray dictionary representation
    description = "A multi dimensional hypercube with configurable dimensions."
    type = "object"
    required = ["id", "data", "dimension"]
    properties = {
        "id": {
            "description": "The identifier of this hyper cube.",
            "type": "string"
        },

        "data": {
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
                "type": Dimension
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


#####################################################################

class FeatureCollectionTile(Schema):
    description = "A tile of vector data that represents a " \
                  "spatio-temporal subset of a spatio-temporal " \
                  "vector dataset. "
    type = "object"
    required = ["data", "id"]
    properties = {
        "id": {
            "description": "The identifier of this vector tile.",
            "type": "string"
        },
        "data": {
            "description": "A GeoJSON FeatureCollection.",
            "type": dict()
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
            "items": {"type": "string"}
        }
    }
    example = {
        "id": "test_data",
        "start_times": ["2001-01-01T00:00:00",
                        "2001-01-02T00:00:00"],
        "end_times": ["2001-01-02T00:00:00",
                      "2001-01-03T00:00:00"],
        "data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                               "geometry": {"coordinates": [24.0, 50.0], "type": "Point"}},
                              {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                               "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
                 "type": "FeatureCollection"}
    }


#####################################################################

class StructuredData(Schema):
    description = "This model represents structured data that is produced by an UDF and can not be represented" \
                  "as a RasterCollectionTile or FeatureCollectionTile. For example the result of a statistical " \
                  "computation. The data is self descriptive and supports the basic types dict/map, list and table."
    type = "object"
    required = ["description", "data", "type"]
    properties = {
        "description": {
            "type": "string",
            "description": "A detailed description of the output format.",
        },
        "data": {
            "type": dict(),
            "description": "The structured data. This field contains the UDF specific values (argument or return)"
                           "as dict, list or table. "
                           "  * A dict can be as complex as required by the UDF."
                           "  * A list must contain simple data types example {\"list\": [1,2,3,4]} "
                           "  * A table is a list of lists with a header, example {\"table\": [[\"id\",\"value\"],"
                           "                                                                     [1,     10],"
                           "                                                                     [2,     23],"
                           "                                                                     [3,     4]]}"
        },
        "type": {
            "type": "string",
            "description": "The type of the structured data that may be of type dict, table or list. "
                           "This is just a hint for the user how to interpret the provided data.",
            "enum": ["dict", "table", "list"]
        }
    }
    example = {"description": "Output of a statistical analysis. The univariate analysis "
                              "of multiple raster collection tiles. Each entry in the output dict/map contains "
                              "min, mean and max of all pixels in a raster collection tile. The key "
                              "is the id of the raster collection tile.",
               "data": {"RED":{"min":0, "max":100, "mean":50}, "NIR":{"min":0, "max":100, "mean":50}},
               "type": "dict"}


#####################################################################

class MachineLearnModel(Schema):
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
        "md5": {
            "type": "string",
            "description": "The md5 checksum of the model that should be used to identify "
                           "the machine learn model in the UDF system. The machine learn model must be "
                           "uploaded to the UDF server."
        }
    }
    example = {"framework": "sklearn",
               "name": "random_forest",
               "description": "A random forest model",
               "path": "/tmp/model.pkl.xz"}


#####################################################################

class UdfData(Schema):
    description = "The UDF data object that stores raster collection tiles, feature collection tiles," \
                  "projection information and machine learn models. This object is argument for the " \
                  "UDF as well as their return value."
    type = "object"
    required = ["proj"]
    properties = {
        "proj": {
            "type": "string",
            "description": "The EPSG code or WKT projection string. eg: EPSG:4326"
        },
        "raster_collection_tiles": {
            "description": "A list of raster collection tiles. Each tile represents a single "
                           "image band or other scalar values like temperature.",
            "type": "array",
            "items": RasterCollectionTile
        },
        "feature_collection_tiles": {
            "description": "A list of feature collection tiles.",
            "type": "array",
            "items": FeatureCollectionTile
        },
        "hypercubes": {
            "description": "A list of hyper cubes.",
            "type": "array",
            "items": HyperCube
        },
        "structured_data_list": {
            "description": "A list of structured data objects that contain processing results that cant be represented "
                           "by raster- or feature collection tiles.",
            "type": "array",
            "items": StructuredData
        },
        "machine_learn_models": {
            "description": "A list of machine learn models.",
            "type": "array",
            "items": MachineLearnModel
        }
    }
    example = {
        "proj": "EPSG:4326",
        "raster_collection_tiles": [
            {
                "id": "RED",
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
        ],
        "feature_collection_tiles": [
            {
                "id": "test_data",
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                                       "geometry": {"coordinates": [24.0, 50.0], "type": "Point"}},
                                      {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                                       "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
                         "type": "FeatureCollection"}
            }
        ],
        "structured_data": [
            {"description": "Output of a statistical analysis. The univariate analysis "
                            "of multiple raster collection tiles. Each entry in the output dict/map contains "
                            "min, mean and max of all pixels in a raster collection tile. The key "
                            "is the id of the raster collection tile.",
             "data": {"RED": {"min": 0, "max": 100, "mean": 50},
                      "NIR": {"min": 0, "max": 100, "mean": 50}},
             "type": "dict"},
            {"description": "A list of values.",
             "data": {"list": [1,2,3,4,5]},
             "type": "list"},
            {"description": "A list of values.",
             "data": {"table": [["id","value"], [1, 10], [2, 23], [3, 4]]},
             "type": "table"}
        ],
        "machine_learn_models": [
            {"framework": "sklearn",
             "name": "random_forest",
             "description": "A random forest model",
             "path": "/tmp/model.pkl.xz"
            }
        ]
    }


# The following classes are used to implement the UDF test server POST endpoint

class UdfCode(Schema):
    description = "The object that stores the UDF code and language specification. This class is not part of the UDF " \
                  "API but used to create the UDF test server."
    type = "object"
    required = ["language", "source"]
    properties = {
        "language": {
            "type": "string",
            "description": "The language of UDF code"
        },
        "source": {
            "type": "string",
            "description": "The UDF source code as a string"
        }
    }
    example = {
        "language": "python",
        "source": "import numpy as np \n"
                " \n"
                "def udf(data): \n"
                "    pass\n"
    }


class UdfRequest(Schema):
    description = "The udf request JSON specification.  This class is not part of the UDF " \
                  "API but used to create the UDF test server."
    type = "object"
    required = ["code", "data"]
    properties = {
        "code": UdfCode,
        "data": UdfData
    }


class ErrorResponse(Schema):
    description = "The error message. This class is not part of the UDF " \
                  "API but used to create the UDF test server."
    type = "object"
    required = ["message"]
    properties = {
        "message": {
            "type": "string",
            "description": "The error message"
        },
        "traceback": {
            "type": "string",
            "description": "The optional python traceback"
        }
    }
