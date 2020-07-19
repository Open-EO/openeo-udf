# -*- coding: utf-8 -*-
from pydantic import BaseModel, Schema as pydSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


EXAMPLE = {"framework": "sklearn",
           "name": "random_forest",
           "description": "A random forest model",
           "path": "/tmp/model.pkl.xz"}


class MachineLearnModel(BaseModel):
    """A machine learn model that should be applied to the UDF data."""

    framework: str = pydSchema(..., description="The framework that was used to train the model",
                               enum=["sklearn", "pytorch", "tensorflow", "R"],
                               examples=[{"framework": "sklearn"}])

    name: str = pydSchema(..., description="The name of the machine learn model.")

    description: str = pydSchema(..., description="The description of the machine learn model.")

    path: str = pydSchema(None, description="The path to the machine learn model file "
                                            "to which the UDF must have read access.")

    md5_hash: str = pydSchema(None, description="The md5 checksum of the model that should be used to identify "
                                                "the machine learn model in the UDF storage system. "
                                                "The machine learn model must be uploaded to the UDF server.")

    class Config:
        schema_extra = {
            'examples': [EXAMPLE]
        }
