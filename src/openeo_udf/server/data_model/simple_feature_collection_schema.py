# -*- coding: utf-8 -*-
from typing import List, Union, Dict

from pydantic import BaseModel, Schema as Field

from openeo_udf.server.data_model.bounding_box_schema import SpatialBoundingBoxModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class SimpleFeatureModel(BaseModel):
    """A simple feature definition that may contain (multi)points, (multi)lines or (multi)polygons"""
    type: str = Field(...,
                      description="The type of the simple feature: Point, LineString, "
                                  "Polygon, MultiPoint, MultiLine, MultiPolygon.")
    predecessors: List[int] = Field(None, description="A list of predecessors from which this feature was created.")
    geometry: int = Field(..., description="The index of a geometry from the geometry collection.")
    variable: List[int] = Field(None, description="The index of the assigned "
                                                  "field collection and the value/label index.")
    timestamp: int = Field(None, description="The index of the assigned timestamp.")


class SimpleFeatureCollectionModel(BaseModel):
    """Simple feature collection: (multi)points, (multi)lines or (multi)polygons"""
    name: str = Field(...,
                      description="The unique name of the simple feature collection."
                                  " Allowed characters [a-z][A-Z][0-9][_].",
                      examples=[{"name": "borders_1984"}])
    description: str = Field(None, description="Description.")
    number_of_features: int = Field(..., description="The number of features.")
    bbox: SpatialBoundingBoxModel = Field(..., description="The bounding box of all features.")
    reference_system: Union[str, int, Dict] = Field(None,
                                                    description="The definition of the spatial reference system. If an "
                                                                "integer was provided it will be interpreted "
                                                                "as EPSG code. If a string was provided it will "
                                                                "be interpreted as WKT2 definition. In case of a "
                                                                "dictionary object, PROJSON is expected. "
                                                                "The definition is identical to the dimension srs")
    features: List[SimpleFeatureModel] = Field(..., description="A list of features.")
