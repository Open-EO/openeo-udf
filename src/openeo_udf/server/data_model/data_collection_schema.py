# -*- coding: utf-8 -*-
from typing import List, Union, Tuple

from pydantic import BaseModel, Schema as Field

from openeo_udf.server.data_model.datacube_schema import DataCubeModel
from openeo_udf.server.data_model.variables_collection_schema import VariablesCollectionModel
from openeo_udf.server.data_model.metadata_schema import MetadataModel
from openeo_udf.server.data_model.simple_feature_collection_schema import SimpleFeatureCollectionModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class TimeStampsModel(BaseModel):
    """The time stamps of the data collections"""
    intervals: List[Tuple[str, Union[str, None]]] = Field(..., description="A list of timestamp tuples as strings. "
                                                                           "Here start and end time can be specified. "
                                                                           "If only the start time is given, then the "
                                                                           "end time can be None.")
    calendar: str = Field(None, description="The definition of the temporal reference system of "
                                            "the  time stamps. Either the gregorian or julian calendar.")


class ObjectCollectionModel(BaseModel):
    """Object collection that contains data cubes and simple feature collections"""
    data_cubes: List[DataCubeModel] = Field(None, description="A list of data cubes")
    simple_feature_collections: List[SimpleFeatureCollectionModel] = Field(None,
                                                                           description="A list of simple "
                                                                                  "features collections")


class DataCollectionModel(BaseModel):
    """Data collection"""
    type: str = "DataCollection"
    metadata: MetadataModel = Field(..., description="The metadata object for the data collection")
    object_collections: ObjectCollectionModel = Field(...,
                                                      description="A collection of different "
                                                                 "data objects like data cubes and feature collections")
    geometry_collection: List[str] = Field(...,
                                           description="A list of WKT geometry strings that are referenced by the "
                                                       "objects in the object collection.")
    variables_collections: List[VariablesCollectionModel] = Field(..., description="A list of variable collections")
    timestamps: TimeStampsModel = Field(..., description="The time stamps of the data collection, that can be references "
                                                         "by each object (feature, cube, ...).")

