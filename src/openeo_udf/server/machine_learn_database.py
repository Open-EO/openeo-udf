# -*- coding: utf-8 -*-
from pydantic import BaseModel, Schema
import os
from shutil import copyfile
from hashlib import md5
from typing import Optional

from openeo_udf.server.config import UdfConfiguration

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ResponseStorageModel(BaseModel):

    md5_hash: str = Schema(..., description="The md5 checksum of the stored model.")
    source: str = Schema(..., description="The source of the machine learn model.")
    title: str = Schema(None, description="The title of the machine learn model.")
    description: str = Schema(None, description="The description of the machine learn model.")


class RequestStorageModel(BaseModel):

    uri: str = Schema(..., description="The local path to a machine learn model or an URL "
                                       "where the model can be downloaded from.",
                      examples=["/tmp/local_model.zip", "ftp://ftp.company.com/model/my_model.zip"])
    title: str = Schema(None, description="The title of the machine learn model.")
    description: str = Schema(None, description="The description of the machine learn model.")


def store_model(filepath: str, request_storage: RequestStorageModel) -> Optional[str]:
    if os.path.exists(filepath) and os.path.isfile(filepath):

        model_file = open(filepath, "rb")
        md5_hash = md5(model_file.read()).hexdigest()
        model_file.close()

        md5_hash_path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)

        if os.path.exists(md5_hash_path):
            return md5_hash

        response_model = ResponseStorageModel(md5_hash=md5_hash, source=request_storage.uri,
                                              title=request_storage.title,
                                              description=request_storage.description)

        meta_file = open(md5_hash_path + ".json", "w")
        meta_file.write(response_model.json())
        meta_file.close()

        copyfile(filepath, md5_hash_path)
        return md5_hash
    return None
