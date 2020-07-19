# -*- coding: utf-8 -*-
from typing import List, Union

from pydantic import BaseModel, Schema as pyField

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class VariableModel(BaseModel):
    """This represents a variable definition with values and labels"""
    name: str = pyField(...,
                        description="Name of the variable.")
    description: str = pyField(None, description="Description of the variable.")
    unit: str = pyField(...,
                        description="The unit of the variable.",
                        examples=[{"unit": "m"}, {"unit": "NDVI"}, {"unit": "Watt"}])
    values: List[Union[float, int]] = pyField(...,
                                              description="The variable values that must be numeric.",
                                              examples=[{"values": [1, 2, 3]}])
    labels: List[str] = pyField(...,
                                description="Label for each variable value.",
                                examples=[{"labels": ["a", "b", "c"]}])


class VariablesCollectionModel(BaseModel):
    """A collection of variables that all have the same size"""
    name: str = pyField(..., description="Name of the variables collection.")
    size: List[int] = pyField(..., description="The size of the variables collection. Each variable of "
                                               "this collection must have the same size. The size of "
                                               "the variable can be mutli-dimensional. However, variables are stored "
                                               "as one dimensional arrays and must be "
                                               "re-shaped in the multi-dimensional form for processing.",
                              examples=[{"size": [100]}, {"size": [3, 3, 3]}])
    number_of_variables: int = pyField(..., description="The number of variables in this collection.")
    variables: List[VariableModel] = pyField(..., description="A list of variables with the same size.")
