# -*- coding: utf-8 -*-
from typing import List, Union

from pydantic import BaseModel, Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DimensionModel(BaseModel):
    """Description of a single dimension"""

    name: str = Schema(...,
                       description="The name of the dimension, like *time*, *X*, *Y*, *Z* and so on.",
                       examples=[{"name": "time"}])

    description: str = Schema(None, description="Description of the dimension.")

    unit: str = Schema(None,
                       description="The unit of the dimension. The unit can be *ISO:8601* for time; "
                                   "metric length units based on meter: *nm* (nanometer), "
                                   "*mm* (millimeter), *cm* (centimeter), "
                                   "*m* (meter), *dm* (decimeter), *km* (kilometer); "
                                   "temperature *K* (Kelvin), *C* (degree Celsius);"
                                   "lat-lon coordinates in *degree*;"
                                   "earth observation units: NDVI, DVI, ... ; "
                                   "sensor units: *int8*, *int16*, *int32*; "
                                   "user defined units: *user_lala* ",
                       examples=[{"unit": "ISO:8601"}])

    coordinates: List[Union[int, float, str]] = Schema(None,
                                                       description="The array that contains the coordinates "
                                                                   "of the specific dimension. "
                                                                   "This parameter is optional.",
                                                       examples=[{"coordinates": ["2001-01-01", "2001-01-02"]}])
