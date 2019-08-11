# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

from openeo_udf.server.feature_collection_tile_schema import FeatureCollectionTileSchema
from openeo_udf.server.hypercube_schema import HyperCubeSchema
from openeo_udf.server.machine_learn_schema import MachineLearnModelSchema
from openeo_udf.server.raster_collection_tile_schema import RasterCollectionTileSchema
from openeo_udf.server.structured_data_schema import StructuredDataSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfDataSchema(Schema):
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
            "items": RasterCollectionTileSchema
        },
        "feature_collection_tiles": {
            "description": "A list of feature collection tiles.",
            "type": "array",
            "items": FeatureCollectionTileSchema
        },
        "hypercubes": {
            "description": "A list of hyper cubes.",
            "type": "array",
            "items": HyperCubeSchema
        },
        "structured_data_list": {
            "description": "A list of structured data objects that contain processing results that cant be represented "
                           "by raster- or feature collection tiles.",
            "type": "array",
            "items": StructuredDataSchema
        },
        "machine_learn_models": {
            "description": "A list of machine learn models.",
            "type": "array",
            "items": MachineLearnModelSchema
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

class UdfCodeSchema(Schema):
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


class UdfRequestSchema(Schema):
    description = "The udf request JSON specification.  This class is not part of the UDF " \
                  "API but used to create the UDF test server."
    type = "object"
    required = ["code", "data"]
    properties = {
        "code": UdfCodeSchema,
        "data": UdfDataSchema
    }


class ErrorResponseSchema(Schema):
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
