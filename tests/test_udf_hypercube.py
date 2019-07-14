# -*- coding: utf-8 -*-
from typing import Tuple

from flask import json
import os
import pprint
import unittest
import xarray
import numpy
import msgpack
import base64
from openeo_udf.server.app import flask_api
from openeo_udf.server.endpoints import create_endpoints
from openeo_udf.server.definitions import UdfCode, UdfRequest
from openeo_udf.api.base import UdfData, HyperCube
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_hypercube(name:str, value: float,shape: Tuple=(3,3,3), dims: Tuple=( "time", "x", "y")) -> HyperCube:
    """Create a hypercube from shape and dimension parameter. The number of shapes and
    dimensions must be equal."""

    coords = {}
    for dim, size in zip(dims, shape):
        coords[dim] = list(range(size))

    array = xarray.DataArray(numpy.zeros(shape=shape), coords=coords, dims=dims)
    array.data += value
    array.name = name
    hc = HyperCube(array=array)

    return hc


class AllTestCase(unittest.TestCase):
    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()

    def test_hypercube_ndvi(self):
        """Test the hypercube NDVI computation"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_ndvi.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())

        hc_red = create_hypercube(name="red", value=1, shape=(3, 3, 3))
        hc_nir = create_hypercube(name="nir", value=3, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[hc_red, hc_nir])

        udf_request = UdfRequest(data=udf_data.to_dict(), code=udf_code)
        pprint.pprint(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        dict_data = json.loads(response.data)
        pprint.pprint(dict_data)
        self.checkHyperCube(dict_data=dict_data)

    def test_hypercube_ndvi_message_pack(self):
        """Test the hypercube NDVI computation with the message pack protocol"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_ndvi.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())

        hc_red = create_hypercube(name="red", value=1, shape=(3, 3, 3))
        hc_nir = create_hypercube(name="nir", value=3, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[hc_red, hc_nir])

        udf_request = UdfRequest(data=udf_data.to_dict(), code=udf_code)
        # pprint.pprint(udf_request)

        udf_request = base64.b64encode(msgpack.packb(udf_request, use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request, content_type="application/base64")

        blob = base64.b64decode(response.data)
        dict_data = msgpack.unpackb(blob, raw=False)
        self.checkHyperCube(dict_data=dict_data)

    def checkHyperCube(self, dict_data):
        """Check the hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc_ndvi: HyperCube = udata.hypercube_list[0]
        self.assertEqual(hc_ndvi.id, "NDVI")
        self.assertEqual(hc_ndvi.array.name, "NDVI")
        self.assertEqual(hc_ndvi.array.data.shape, (3, 3, 3))
        self.assertEqual(hc_ndvi.array.data[0][0][0], 0.5)
        self.assertEqual(hc_ndvi.array.data[2][2][2], 0.5)


if __name__ == "__main__":
    unittest.main()
