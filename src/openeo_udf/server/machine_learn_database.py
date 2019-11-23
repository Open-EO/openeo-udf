# -*- coding: utf-8 -*-
import pprint
import traceback
import sys
import os
from shutil import copyfile
from hashlib import md5
from os import listdir
from os.path import isfile, join
from typing import Optional, List

import requests
from fastapi import HTTPException
from pydantic import BaseModel, Schema
from starlette.responses import PlainTextResponse
import ujson
from openeo_udf.server.app import app
from openeo_udf.server.data_model.udf_schemas import ErrorResponseModel
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


@app.get("/storage", response_model=List[ResponseStorageModel],
         responses={200: {"content": {"application/json": {}},
                          "description": "A list of metadata information about the stored machine model that include "
                                         "the md5 hash, the source, the title and the description.."},
                    400: {"content": {"application/json": {}}}})
async def ml_get():
    """Return all md5 hashes of the stored machine learn models as list
    """
    try:
        path = UdfConfiguration.machine_learn_storage_path
        if os.path.isdir(path):

            result = []
            file_list = [f for f in listdir(path) if isfile(join(path, f))]

            for f in file_list:
                if ".json" in f:
                    meta_file = open(join(path, f), "r")
                    d = ujson.loads(meta_file.read())
                    pprint.pprint(d)
                    model = ResponseStorageModel(**d)
                    result.append(model)

            return result

        response = ErrorResponseModel(message=f"The storage path of the machine learn models was not found on server.")
        raise HTTPException(status_code=400, detail=response)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


@app.delete("/storage/{md5_hash}", response_model=str, responses={200: {"content": {"text/plain": {}},
                                                                        "description": "The removed md5 hash"},
                                                                  400: {"content": {"application/json": {}}}})
async def ml_delete(md5_hash: str):
    """
    Delete a machine learn model in the udf machine learn database
    that matches the provided md5 hash. The md5 hash of the to be deleted model
    must be provided as text in the HTTP request.
    """

    try:
        path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)
        if os.path.exists(path):
            os.remove(path)
            # Remove the json file
            if os.path.exists(path + ".json"):
                os.remove(path + ".json")

            return PlainTextResponse(md5_hash)

        response = ErrorResponseModel(message=f"The machine learn model for hash {md5_hash} was not found")
        raise HTTPException(status_code=400, detail=response.dict())
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


class RequestStorageModel(BaseModel):

    uri: str = Schema(..., description="The local path to a machine learn model or an URL "
                                       "where the model can be downloaded from.",
                      examples=["/tmp/local_model.zip", "ftp://ftp.company.com/model/my_model.zip"])
    title: str = Schema(None, description="The title of the machine learn model.")
    description: str = Schema(None, description="The description of the machine learn model.")


@app.post("/storage", response_model=str, responses={200: {"content": {"text/plain": {}},
                                                           "description": "The generated md5 hash"},
                                                     400: {"content": {"application/json": {}}}})
async def ml_post(request_storage: RequestStorageModel):
    """
    Store a machine learn model in the udf machine learn database
    and return the corresponding md5 hash. The URL were the model is located
    must be provided as text in the HTTP request
    """

    try:
        if os.path.exists(request_storage.uri):
            filepath = request_storage.uri
        else:
            # Check if thr URL exists by investigating the HTTP header
            resp = requests.head(request_storage.uri, allow_redirects=True)

            if resp.status_code != 200:
                raise Exception("The URL <%s> can not be accessed." % request_storage.uri)

            filename = request_storage.uri.rsplit('/', 1)[1]
            filepath = os.path.join(UdfConfiguration.temporary_storage_path, filename)

            print(request_storage)

            r = requests.get(request_storage.uri, allow_redirects=True)
            model_file = open(filepath, 'wb')
            model_file.write(r.content)
            model_file.close()

        md5_hash = store_model(filepath=filepath, request_storage=request_storage)
        if md5_hash:
            return PlainTextResponse(md5_hash)

        response = ErrorResponseModel(message=f"Unable to access machine learn model at {request_storage.uri}")
        raise HTTPException(status_code=400, detail=response.dict())
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


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
