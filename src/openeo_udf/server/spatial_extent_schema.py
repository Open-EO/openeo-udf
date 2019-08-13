# -*- coding: utf-8 -*-
from pydantic import BaseModel, Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


EXAMPLE = {
    "extent": {
        "top": 53,
        "bottom": 50,
        "right": 30,
        "left": 24,
        "height": 0.01,
        "width": 0.01
    }
}


class SpatialExtentModel(BaseModel):
    """spatial extent with resolution information"""

    top: float = Schema(..., description="The top (north) border.")
    bottom: float = Schema(..., description="The bottom (south) border.")
    right: float = Schema(..., description="The right (eastern) border.")
    left: float = Schema(..., description="The left (wester) border.")
    height: float = Schema(..., description="The top-bottom resolution in projection units.")
    width: float = Schema(..., description="The right-left resolution in projection units.")

    class Config:
        schema_extra = {
            'examples': [EXAMPLE]
        }
