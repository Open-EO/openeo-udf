# -*- coding: utf-8 -*-
from typing import List
from pydantic import BaseModel, Schema

from openeo_udf.server.data_model.legacy.feature_collection_legacy_schema import FeatureCollectionLegacyModel
from openeo_udf.server.data_model.legacy.datacube_legacy_schema import DataCubeLegacyModel
from openeo_udf.server.data_model.machine_learn_schema import MachineLearnModel
from openeo_udf.server.data_model.structured_data_schema import StructuredDataModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfLegacyDataModel(BaseModel):
    """
    The UDF data object that feature collections, data cubes,,
    projection information and machine learn models. This object is argument for the
    UDF as well as their return value.
    """

    proj: dict = Schema(..., description="The EPSG code or WKT projection dictionary. eg: {'EPSG':4326}")

    user_context: dict = Schema({}, description="A dictionary that contains the user context, "
                                                "like function parameters or configuration of an algorithm.")

    server_context: dict = Schema({}, description="A dictionary that contains the server context")

    feature_collection_list: List[FeatureCollectionLegacyModel] = Schema([],
                                                                         description="A list of feature "
                                                                               "collection tiles.")

    datacubes: List[DataCubeLegacyModel] = Schema([], description="A list of data cubes.")

    structured_data_list: List[StructuredDataModel] = Schema([], description="A list of structured data objects "
                                                                             "that contain processing results that "
                                                                             "cant be represented "
                                                                             "by raster- or feature "
                                                                             "collection tiles.")

    machine_learn_models: List[MachineLearnModel] = Schema([], description="A list of machine learn models.")


# The following classes are used to implement the UDF test server POST endpoint
class UdfLegacyCodeModel(BaseModel):
    """
    The object that stores the UDF code and language specification. This class is not part of the UDF
    API but used to create the UDF test server."
    """

    language: str = Schema(..., description="The language of UDF code")
    source: str = Schema(..., description="The UDF source code as a string")


class UdfLegacyRequestModel(BaseModel):
    """
    The udf request JSON specification.  This class is not part of the UDF API but used to create the UDF test server.
    """
    code: UdfLegacyCodeModel
    data: UdfLegacyDataModel
