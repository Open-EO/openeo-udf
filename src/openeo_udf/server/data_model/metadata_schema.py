# -*- coding: utf-8 -*-
from pydantic import BaseModel, Schema as Field


__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class MetadataModel(BaseModel):
    """Metadata description of the topological data collection"""

    name: str = Field(..., description="The name of topological data collection. "
                                       "Allowed characters [a-z][A-Z][0-9][_].",
                      examples=[{"name": "Climate_data_collection_1984"}])
    description: str = Field(..., description="Description of the topological data collection.")
    number_of_object_collections: int = Field(..., description="Number of all collections "
                                                               "(data cubes, image collection, "
                                                               "simple feature collections,"
                                                               "topological feature collections).")
    number_of_geometries: int = Field(..., description="Number of all geometries.")
    number_of_variable_collections: int = Field(..., description="Number of all variable collections.")
    number_of_time_stamps: int = Field(..., description="Number of time tamps.")
    creator: str = Field(None, description="The name of the creator.")
    creation_time: str = Field(None, description="Time of creation.")
    modification_time: str = Field(None, description="Time of last modification.")
    source: str = Field(None, description="The source of the data collections.")
    link: str = Field(None, description="URL link to a specific web source.")
    userdata: dict = Field(None, description="A dictionary of additional metadata (STAC).")
