# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Schema
from openeo_udf.server.data_model.machine_learn_schema import MachineLearnModel
from openeo_udf.server.data_model.structured_data_schema import StructuredDataModel
from openeo_udf.server.data_model.data_collection_schema import DataCollectionModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfDataModel(BaseModel):
    """
    The UDF data object that stores data cubes, simple feature collection and machine learn models.
    This object is argument for the UDF as well as their return value.
    """

    user_context: dict = Schema({}, description="A dictionary that contains the user context, "
                                                "like function parameters or configuration of an algorithm.")

    server_context: dict = Schema({}, description="A dictionary that contains the server context")

    data_collection: DataCollectionModel = Schema([], description="The data collection with data cubes and "
                                                                  "simple feature collections.")

    structured_data_list: List[StructuredDataModel] = Schema([], description="A list of structured data objects "
                                                                             "that contain processing results that "
                                                                             "cant be represented "
                                                                             "by raster- or feature "
                                                                             "collection tiles.")

    machine_learn_models: List[MachineLearnModel] = Schema([], description="A list of machine learn models.")


# The following classes are used to implement the UDF test server POST endpoint

class UdfCodeModel(BaseModel):
    """
    The object that stores the UDF code and language specification. This class is not part of the UDF
    API but used to create the UDF test server."
    """

    language: str = Schema(..., description="The language of UDF code")
    source: str = Schema(..., description="The UDF source code as a string")


class UdfRequestModel(BaseModel):
    """
    The udf request JSON specification.  This class is not part of the UDF API but used to create the UDF test server.
    """
    code: UdfCodeModel
    data: UdfDataModel


class ErrorResponseModel(BaseModel):
    """
    The error message. This class is not part of the UDF API but used to create the UDF test server."
    """

    message: str = Schema(..., description="The error message")

    traceback: str = Schema(None, description="The optional python traceback")
