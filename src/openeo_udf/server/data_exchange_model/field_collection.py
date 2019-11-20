# -*- coding: utf-8 -*-
from typing import List, Union

from pydantic import BaseModel, Schema as pyField

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Field(BaseModel):
    """This represents a field definition with values and labels"""
    name: str = pyField(...,
                        description="Name of the attribute.")
    description: str = pyField(None, description="Description of the attribute.")
    unit: str = pyField(...,
                        description="The unit of the field.",
                        examples=[{"unit": "m"}, {"unit": "NDVI"}, {"unit": "Watt"}])
    values: List[Union[float, int]] = pyField(...,
                                              description="The field values that must be numeric.",
                                              examples=[{"values": [1, 2, 3]}])
    labels: List[str] = pyField(...,
                                description="Label for each field value.",
                                examples=[{"labels": ["a", "b", "c"]}])


class FieldCollection(BaseModel):
    """A collection of fields that all have the same size"""
    name: str = pyField(..., description="Name of the field collection.")
    size: List[int] = pyField(..., description="The size of the field collection. Each field of "
                                               "this collection must have the same size. The size of "
                                               "the fields can be mutli-dimensional. However, fields are stored "
                                               "as one dimensional array and must be "
                                               "re-shaped in the multi-dimensional form for processing.",
                              examples=[{"size": [100]}, {"size": [3, 3, 3]}])
    number_of_fields: int = pyField(..., description="The number of fields in this collection." )
    attributes: List[Field] = pyField(..., description="A list of fields with the same size.",
                                      alias="fields")
