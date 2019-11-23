# -*- coding: utf-8 -*-
import traceback
import sys

import msgpack
import base64
from fastapi import HTTPException, Body
from starlette.responses import PlainTextResponse
from starlette.requests import Request

from openeo_udf.server.app import app
from openeo_udf.server.data_model.udf_schemas import UdfRequestModel, ErrorResponseModel, UdfDataModel
from openeo_udf.api.run_code import run_json_user_code

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


@app.post("/udf", response_model=UdfDataModel, responses={200: {"content": {"application/json": {"example": ""}},
                                                                "description": "The processed data"},
                                                          400: {"content": {"application/json": {}}}})
async def udf_json(request: UdfRequestModel = Body(...)):
    """Run a Python user defined function (UDF) on the provided data"""

    try:
        result = run_json_user_code(dict_data=request.dict())
        return result
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())


@app.post("/udf_message_pack", response_model=str, responses={200: {"content": {"application/base64": {}},
                                                                    "description": "The base64 encoded string"},
                                                              400: {"content": {"application/json": {}}}})
async def udf_message_pack(request: Request):
    """Run a Python user defined function (UDF) on the provided data that are base64 encoded message pack objects"""

    try:
        data = await request.body()
        blob = base64.b64decode(data)
        dict_data = msgpack.unpackb(blob, raw=False)
        result = run_json_user_code(dict_data=dict_data)
        result = base64.b64encode(msgpack.packb(result))
        return PlainTextResponse(result)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response.dict())
