# -*- coding: utf-8 -*-
import msgpack
import base64
from fastapi import FastAPI
from fastapi import Body
from starlette.requests import Request
import pprint
import traceback
import sys
import os
from os import listdir
from os.path import isfile, join
from typing import List

import requests
from fastapi import HTTPException
from starlette.responses import PlainTextResponse
import ujson
from openeo_udf.server.config import UdfConfiguration
from openeo_udf.server.data_model.legacy.udf_legacy_schemas import UdfLegacyDataModel, UdfLegacyRequestModel

from openeo_udf.server.data_model.udf_schemas import UdfRequestModel, ErrorResponseModel, UdfDataModel
from openeo_udf.api.run_code import run_legacy_user_code, run_udf_model_user_code
from openeo_udf.server.machine_learn_database import ResponseStorageModel, RequestStorageModel, store_model

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

"""
There are several different approached available in python that can be implemented:
- UBJSON https://en.wikipedia.org/wiki/UBJSON
- BSON https://en.wikipedia.org/wiki/BSON
- MessagePack https://en.wikipedia.org/wiki/MessagePack

Important is the support for arrays with integer and floating point numbers that are used in
xarray and numpy. Support for timestamps is required as well. For structured data is the support of lists
and maps important.

              array integer float map time

MessagePack     y      y      y    y    y
BJSON           y      y      y    y    n
UBJSON          n      y      y    n    n

Based on these requirement it seems that MessagePack is the most potent candidate to use
for serialization and supports many different languages.
MessagePack is available here: https://msgpack.org/

Using Messagepack is quite easy:

In [1]: import msgpack
In [2]: import base64
In [3]: d = {1:[1,2,3,4,5,6], "w":"fffff", "d":{"d":"d"}}
In [4]: d
Out[4]: {1: [1, 2, 3, 4, 5, 6], 'w': 'fffff', 'd': {'d': 'd'}}
In [5]: msgpack.packb(d)
Out[5]: b'\x83\x01\x96\x01\x02\x03\x04\x05\x06\xa1w\xa5fffff\xa1d\x81\xa1d\xa1d'
In [6]: p = msgpack.packb(d)
In [7]: base64.b64encode(p)
Out[7]: b'gwGWAQIDBAUGoXelZmZmZmahZIGhZKFk'
In [8]: t = base64.b64encode(p)
In [9]: base64.b64decode(t)
Out[9]: b'\x83\x01\x96\x01\x02\x03\x04\x05\x06\xa1w\xa5fffff\xa1d\x81\xa1d\xa1d'
In [10]: msgpack.unpackb(base64.b64decode(t))
Out[10]: {1: [1, 2, 3, 4, 5, 6], b'w': b'fffff', b'd': {b'd': b'd'}}

"""

app = FastAPI(title="UDF Server for geodata processing",
              description="This server processes UDF data")


@app.post("/udf", response_model=UdfDataModel, tags=["udf"])
async def udf(request: UdfRequestModel = Body(...)):
    """Run a Python user defined function (UDF) on the provided data collection"""

    try:
        result = run_udf_model_user_code(udf_model=request)
        return result
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


@app.post("/udf_message_pack", tags=["udf"], response_model=str,
          responses={200: {"content": {"application/base64": {}},
                           "description": "The base64 encoded string"},
                     400: {"content": {"application/json": {}}}})
async def udf_message_pack(request: Request):
    """Run a Python user defined function (UDF) on the provided data collection
    that are base64 encoded message pack objects"""

    try:
        data = await request.body()
        blob = base64.b64decode(data)
        udf_model: UdfRequestModel = msgpack.unpackb(blob, raw=False)
        result = run_udf_model_user_code(udf_model=udf_model)
        result = base64.b64encode(msgpack.packb(result.to_dict()))
        return PlainTextResponse(result)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


@app.post("/udf_legacy", response_model=UdfLegacyDataModel, tags=["udf legacy"])
async def udf_legacy(request: UdfLegacyRequestModel = Body(...)):
    """Run a Python user defined function (UDF) on the provided legacy data"""

    try:
        result = run_legacy_user_code(dict_data=request.dict())
        return result
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


@app.post("/udf_legacy_message_pack", response_model=str, tags=["udf legacy"],
          responses={200: {"content": {"application/base64": {}},
                           "description": "The base64 encoded string"},
                     400: {"content": {"application/json": {}}}})
async def udf_legacy_message_pack(request: Request):
    """Run a Python user defined function (UDF) on the provided legacy
    data that are base64 encoded message pack objects"""

    try:
        data = await request.body()
        blob = base64.b64decode(data)
        dict_data = msgpack.unpackb(blob, raw=False)
        result = run_legacy_user_code(dict_data=dict_data)
        result = base64.b64encode(msgpack.packb(result))
        return PlainTextResponse(result)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


@app.get("/storage", response_model=List[ResponseStorageModel], tags=["ML Storage"],
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


@app.delete("/storage/{md5_hash}", response_model=str, tags=["ML Storage"],
            responses={200: {"content": {"text/plain": {}},
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


@app.post("/storage", response_model=str, tags=["ML Storage"], responses={200: {"content": {"text/plain": {}},
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
