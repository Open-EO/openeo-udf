# -*- coding: utf-8 -*-
from typing import List, Union
from pydantic import BaseModel, Schema as Field

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Dimension(BaseModel):
    """Description of a data cube dimension"""
    name: str = Field(..., description="The name/identifier of the dimension.")
    unit: str = Field(...,
                      description="The unit of the dimension in SI units.",
                      examples=[{"unit": "seconds"}, {"unit": "m"}, {"unit": "hours"},
                                {"unit": "days"}, {"unit": "mm"}, {"unit": "km"}])
    size: int = Field(..., description="The size of the dimension.")
    coordinates: List[Union[int, float, str]] = Field(..., description="A list of coordinates for this dimension")


class DataCube(BaseModel):
    """A multidimensional representation of a data cube"""
    name: str = Field(...,
                      description="The unique name of the data cube. Allowed characters [a-z][A-Z][0-9][_].",
                      examples=[{"name": "Climate_data_cube_1984"}])

    description: str = Field(None, description="Description of the data cube.")
    dim: List[str] = Field(...,
                            description="A an ordered list of dimension names of the data cube. The dimensions "
                                        "are applied in the provided order.",
                            examples=[{"dim": ["t", "y", "x"]}])
    dimensions: List[Dimension] = Field(..., description="A list of dimension descriptions.")
    field_collection: int = Field(None, description="The integer index of the field collection. All fields and their "
                                                    "values of this collection are assigned to the "
                                                    "data cube and must have the same size")
    timestamp: int = Field(None, description="The integer index of the assigned timestamp from the timestamp array")
