# -*- coding: utf-8 -*-
from typing import List, Union, Dict
from pydantic import BaseModel, Schema as Field


__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DimensionModel(BaseModel):
    """Description of a data cube dimension. See the STAC dimension definition for more details and examples."""
    description: str = Field(..., description="The description of the dimension.")
    type: str = Field(..., description="The type of the dimension (spatial, temporal, bands, other)")
    unit: str = Field(...,
                      description="The unit of the dimension in SI units or UDUNITS. "
                                  "Time instances or intervals are defined as ISO8601 strings",
                      examples=[{"unit": "seconds"}, {"unit": "m"}, {"unit": "hours"},
                                {"unit": "days"}, {"unit": "mm"}, {"unit": "km"}, {"unit": "ISO8601"}])
    extent: List[Union[int, float, str]] = Field(..., description="The spatial or temporal extent of the dimension. "
                                                                  "It must be a tuple of values.")
    values: List[Union[float, str]] = Field(None, description="A list of coordinates for this dimension. Use "
                                                              "ISO8601 to specify time instances and intervals."
                                                              "If spatial axis are irregular, then the values "
                                                              "parameter should be used to specify this axis. "
                                                              "Otherwise the extent and the number of cells "
                                                              "is sufficient.",
                                                 examples=[{"values": [50, 51, 52]},
                                                           {"values": ["2001-01-01T10:00:00 / 2001-01-01T12:00:00",
                                                                       "2001-01-01T12:00:00 / 2001-01-01T14:00:00"]}])
    number_of_cells: int = Field(None, description="The number of cells in the spatial dimension or intervals / "
                                                   "time instances in case of temporal dimension.")
    axis: str = Field(None, description="If the dimension is spatial, then the axis x, y or z can be "
                                        "specified with this parameter.")
    reference_system: Union[str, int, Dict] = Field(None, description="The definition of the coordinate system. If an "
                                                                      "integer was provided, it will be interpreted "
                                                                      "as EPSG code. If a string was provided it will "
                                                                      "be interpreted as WKT2 definition or in case "
                                                                      "of a temporal dimension as the calendar. "
                                                                      "In case of a dictionary object PROJSON "
                                                                      "is expected.")


class DataCubeModel(BaseModel):
    """A multidimensional representation of a data cube"""
    name: str = Field(...,
                      description="The unique name of the data cube. Allowed characters [a-z][A-Z][0-9][_].",
                      examples=[{"name": "Climate_data_cube_1984"}])

    description: str = Field(None, description="Description of the data cube.")
    dim: List[str] = Field(...,
                           description="A an ordered list of dimension names of the data cube. The dimensions "
                                       "are applied in the provided order.",
                           examples=[{"dim": ["time", "y", "x"]}])
    size: List[int] = Field(..., description="The size of the dimensions as an ordered list of integer values.",
                            examples=[[3, 3, 3]])

    dimensions: Dict[str, DimensionModel] = Field(..., description="A dictionary of dimension descriptions. Dimensions are "
                                                                   "references by their name that is the key of the dict. "
                                                                   "The id of the dimension is a string, that should "
                                                                   "follow the convention: t -> time, "
                                                                   "x, y, z -> spatial dimensions.")
    variable_collection: int = Field(None,
                                     description="The integer index of the variable collection. "
                                                 "All variables and their "
                                                 "values of this indexed collection are assigned to the "
                                                 "data cube and must have the same size")
    timestamp: int = Field(None, description="The integer index of the assigned timestamp from the timestamp array")
