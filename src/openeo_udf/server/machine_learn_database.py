# -*- coding: utf-8 -*-
import traceback
import sys
import os
from shutil import copyfile
from hashlib import md5
from os import listdir
from os.path import isfile, join
from typing import Optional, List

import requests
from fastapi import HTTPException, Body
from openeo_udf.server.app import app
from openeo_udf.server.udf_schemas import ErrorResponseModel
from openeo_udf.server.config import UdfConfiguration


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


GET = {
    "description": "Return a list of all md5 hashes of the provided machine learn models",
    "tags": ["UDF", "machine learning"],
    'produces':["application/json"],
    "responses": {
        "200": {
            "description": "A list of md5 hashes of all stored machine learn models.",
        },
        "400": {
            "description": "The error message.",
            "schema": ErrorResponseModel
        }
    }
}


POST = {
    "description": "Store a machine learn model in the udf machine learn database "
                   "and return the corresponding md5 hash. The URL were the model is located "
                   "must be provided as text in the HTTP request",
    "tags": ["UDF", "machine learning"],
    'consumes':['text/plain'],
    'produces':["text/plain"],
    "responses": {
        "200": {
            "description": "The md5 hash of the stred model.",
        },
        "400": {
            "description": "The error message.",
            "schema": ErrorResponseModel
        }
    }
}

DELETE = {
    "description": "Delete a machine learn model in the udf machine learn database "
                   "that matches the provided md5 hash. The md5 hash of the to be deleted model "
                   "must be provided as text in the HTTP request",
    "tags": ["UDF", "machine learning"],
    'consumes':['text/plain'],
    'produces':["text/plain"],
    "responses": {
        "200": {
            "description": "The model was successfully removed.",
        },
        "400": {
            "description": "The model was not found in the storage.",
            "schema": ErrorResponseModel
        }
    }
}


@app.get("/storage", response_model=List[str])
def ml_get():
    """Return all md5 hashes of the stored machine learn models as list
    """
    try:
        path = UdfConfiguration.machine_learn_storage_path
        if os.path.isdir(path):
            hash_list = [f for f in listdir(path) if isfile(join(path, f))]
            return hash_list

        response = ErrorResponseModel(message=f"The storage path of the machine learn models was not found on server.")
        raise HTTPException(status_code=400, detail=response)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response)


@app.delete("/storage/{md5_hash}", response_model=str)
def ml_delete(md5_hash: str):
    """Remove a single machine learn model from the server"""

    try:
        path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)
        if os.path.exists(path):
            os.remove(path)
            return md5_hash

        response = ErrorResponseModel(message=f"The machine learn model for hash {md5_hash} was not found")
        raise HTTPException(status_code=400, detail=response)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response)


@app.delete("/storage", response_model=str)
def ml_post(url: str = Body(...)):
    """Upload a new machine learn model to the UDF machine learn storage"""

    try:
        if os.path.exists(url):
            filepath = url
        else:
            # Check if thr URL exists by investigating the HTTP header
            resp = requests.head(url, allow_redirects=True)

            if resp.status_code != 200:
                raise Exception("The URL <%s> can not be accessed." % url)

            filename = url.rsplit('/', 1)[1]
            filepath = os.path.join(UdfConfiguration.temporary_storage_path, filename)
            r = requests.get(url, allow_redirects=True)
            open(filepath, 'wb').write(r.content)

        md5_hash = compute_md5_hash(filepath)
        if md5_hash:
            return md5_hash

        response = ErrorResponseModel(message=f"Unable to access machine learn model at {url}")
        raise HTTPException(status_code=400, detail=response)
    except Exception:
        e_type, e_value, e_tb = sys.exc_info()
        response = ErrorResponseModel(message=str(e_value), traceback=str(traceback.format_tb(e_tb)))
        raise HTTPException(status_code=400, detail=response)


def compute_md5_hash(filepath: str) -> Optional[str]:

    if os.path.exists(filepath) and os.path.isfile(filepath):
        md5_hash = md5(open(filepath, "rb").read()).hexdigest()
        md5_hash_path = os.path.join(UdfConfiguration.machine_learn_storage_path, md5_hash)

        if os.path.exists(md5_hash_path):
            return md5_hash

        copyfile(filepath, md5_hash_path)
        return md5_hash
    return None
