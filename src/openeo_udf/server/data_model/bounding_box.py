# -*- coding: utf-8 -*-
from pydantic import BaseModel, Schema as Field

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class SpatialBoundingBox(BaseModel):
    """Spatial bounding box definitions"""
    min_x: float = Field(..., description="The minimum x coordinate of the 3d bounding box.")
    max_x: float = Field(..., description="The maximum x coordinate of the 3d bounding box.")
    min_y: float = Field(..., description="The minimum y coordinate of the 3d bounding box.")
    max_y: float = Field(..., description="The maximum y coordinate of the 3d bounding box.")
    min_z: float = Field(..., description="The minimum z coordinate of the 3d bounding box.")
    max_z: float = Field(..., description="The maximum z coordinate of the 3d bounding box.")
