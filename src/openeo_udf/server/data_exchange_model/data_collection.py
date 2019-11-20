# -*- coding: utf-8 -*-
from typing import List, Union, Tuple

from pydantic import BaseModel, Schema as Field

from openeo_udf.server.data_exchange_model.data_cube import DataCube
from openeo_udf.server.data_exchange_model.field_collection import FieldCollection
from openeo_udf.server.data_exchange_model.metadata import Metadata
from openeo_udf.server.data_exchange_model.simple_feature_collection import SimpleFeatureCollection

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CoordinateReferenceSystems(BaseModel):
    """Coordinate reference systems for spatial and temporal coordinates"""
    EPSG: int = Field(None, description="EPSG code", examples=[{"EPSG": 4326}])
    WKT: str = Field(None, description="The WKT description string, if there is no EPSG code")
    temporal: str = Field(None, description="The temporal calender", examples=[{"temporal": "gregorian"}])


class ObjectCollection(BaseModel):
    """Object collection that contains data cubes and simple feature collections"""
    data_cubes: List[DataCube] = Field(None, description="A list of data cubes")
    simple_feature_collections: List[SimpleFeatureCollection] = Field(None,
                                                                      description="A list of simple "
                                                                                  "features collections")


class DataCollection(BaseModel):
    """Data collection"""
    type: str = "DataCollection"
    crs: CoordinateReferenceSystems = Field(..., description="The coordinate reference systems")
    metadata: Metadata = Field(..., description="The metadata object for the data collection")
    object_collections: ObjectCollection = Field(...,
                                                 description="A collection of different "
                                                             "data objects like data cubes and feature collections")
    geometry_collection: List[str] = Field(...,
                                           description="A list of WKT geometry strings that are referenced by the "
                                                       "objects in the object collection.")
    field_collections: List[FieldCollection] = Field(..., description="A list of field collections")
    timestamps: List[Tuple[str, Union[str, None]]] = Field(..., description="A list of timestamp tuples as strings.")
