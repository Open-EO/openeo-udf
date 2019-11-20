# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Schema as Field

from openeo_udf.server.data_exchange_model.bounding_box import SpatialBoundingBox

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class SimpleFeature(BaseModel):
    """A simple feature definition that may contain (multi)points, (multi)lines or (multi)polygons"""
    type: str = Field(...,
                      description="The type of the simple feature: Point, LineString, "
                                  "Polygon, MultiPoint, MultiLine, MultiPolygon.")
    predecessors: List[int] = Field(None, description="A list of predecessors from which this feature was created.")
    geometry: int = Field(..., description="The index of a geometry from the geometry collection.")
    field: List[int] = Field(None, description="The index of the assigned "
                                               "field collection and the value/label index.")
    timestamp: int = Field(None, description="The index of the assigned timestamp.")


class SimpleFeatureCollection(BaseModel):
    """Simple feature collection: (multi)points, (multi)lines or (multi)polygons"""
    name: str = Field(...,
                      description="The unique name of the simple feature collection."
                                  " Allowed characters [a-z][A-Z][0-9][_].",
                      examples=[{"name": "borders_1984"}])
    description: str = Field(None, description="Description.")
    number_of_features: int = Field(..., description="The number of features.")
    bbox: SpatialBoundingBox = Field(..., description="The bounding box of all features.")
    features: List[SimpleFeature] = Field(..., description="A list of features.")
