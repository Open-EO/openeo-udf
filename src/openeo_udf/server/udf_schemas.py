# -*- coding: utf-8 -*-
from typing import List
from pydantic import BaseModel, Schema

from openeo_udf.server.feature_collection_tile_schema import FeatureCollectionTileModel
from openeo_udf.server.hypercube_schema import HyperCubeModel
from openeo_udf.server.machine_learn_schema import MachineLearnModel
from openeo_udf.server.raster_collection_tile_schema import RasterCollectionTileModel
from openeo_udf.server.structured_data_schema import StructuredDataModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


EXAMPLE = {
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
         "data": {"list": [1, 2, 3, 4, 5]},
         "type": "list"},
        {"description": "A list of values.",
         "data": {"table": [["id", "value"], [1, 10], [2, 23], [3, 4]]},
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


class UdfDataModel(BaseModel):
    """
    The UDF data object that stores raster collection tiles, feature collection tiles,
    projection information and machine learn models. This object is argument for the
    UDF as well as their return value.
    """

    proj: dict = Schema(..., description="The EPSG code or WKT projection dictionary. eg: {'EPSG':4326}")

    user_context: dict = Schema({}, description="A dictionary that contains the user context, "
                                                 "like function parameters or configuration of an algorithm.")

    server_context: dict = Schema({}, description="A dictionary that contains the server context")

    raster_collection_tiles: List[RasterCollectionTileModel] = Schema([],
                                                                      description="A list of raster "
                                                                                     "collection tiles."
                                                                                     " Each tile represents a single "
                                                                                     "image band or other scalar "
                                                                                     "values like temperature.")

    feature_collection_tiles: List[FeatureCollectionTileModel] = Schema([],
                                                                        description="A list of feature "
                                                                                       "collection tiles.")

    hypercubes: List[HyperCubeModel] = Schema([], description="A list of hyper cubes.")

    structured_data_list: List[StructuredDataModel] = Schema([], description="A list of structured data objects "
                                                                                  "that contain processing results that "
                                                                                  "cant be represented "
                                                                                  "by raster- or feature "
                                                                                  "collection tiles.")

    machine_learn_models: List[MachineLearnModel] = Schema([], description="A list of machine learn models.")

    class Config:
        schema_extra = {
            'examples': [EXAMPLE]
        }


# The following classes are used to implement the UDF test server POST endpoint

class UdfCodeModel(BaseModel):
    """
    The object that stores the UDF code and language specification. This class is not part of the UDF
    API but used to create the UDF test server."
    """

    language: str = Schema(..., description="The language of UDF code")
    source: str = Schema(..., description="The UDF source code as a string")


class UdfRequestModel(BaseModel):
    """
    The udf request JSON specification.  This class is not part of the UDF API but used to create the UDF test server.
    """
    code: UdfCodeModel
    data: UdfDataModel


class ErrorResponseModel(BaseModel):
    """
    The error message. This class is not part of the UDF API but used to create the UDF test server."
    """

    message: str = Schema(..., description="The error message")

    traceback: str = Schema(None, description="The optional python traceback")
