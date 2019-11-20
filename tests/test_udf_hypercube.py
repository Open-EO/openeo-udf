# -*- coding: utf-8 -*-
import pprint
from typing import Tuple
import os
import unittest
import xarray
import numpy
import msgpack
import base64

from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfCodeModel, UdfRequestModel
from openeo_udf.api.udf_data import UdfData
from openeo_udf.api.hypercube import HyperCube
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
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_hypercube_map_fabs(self):
        """Test the hypercube mapping of the numpy fabs function"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_map_fabs.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_hypercube(name="temp", value=1, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[temp])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        pprint.pprint(response.json())
        self.assertEqual(response.status_code, 200)
        result = response.json()

        pprint.pprint(result)
        self.checkHyperCubeMapFabs(dict_data=result)

    def otest_hypercube_reduce_sum(self):
        """Test the hypercube sum reduction"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_reduce_time_sum.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_hypercube(name="temp", value=1, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[temp])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()

        pprint.pprint(result)
        self.checkHyperCubeSum(dict_data=result)

    def otest_hypercube_reduce_mean(self):
        """Test the hypercube mean reduction"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_reduce_time_mean.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_hypercube(name="temp", value=1, shape=(3, 3, 3))
        prec = create_hypercube(name="prec", value=3, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[temp, prec])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()

        pprint.pprint(result)
        self.checkHyperCubeMean(dict_data=result)

    def otest_hypercube_reduce_min_median_max(self):
        """Test the hypercube min, median, max reduction"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_reduce_time_min_median_max.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_hypercube(name="temp", value=1, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[temp])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()

        pprint.pprint(result)
        self.checkHyperCubeMinMedianMax(dict_data=result)

    def otest_hypercube_ndvi(self):
        """Test the hypercube NDVI computation"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_ndvi.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        hc_red = create_hypercube(name="red", value=1, shape=(3, 3, 3))
        hc_nir = create_hypercube(name="nir", value=3, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[hc_red, hc_nir])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        print(udf_request.json())
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()

        # pprint.pprint(result)
        self.checkHyperCubeNdvi(dict_data=result)

    def otest_hypercube_ndvi_message_pack(self):
        """Test the hypercube NDVI computation with the message pack protocol"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_ndvi.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        hc_red = create_hypercube(name="red", value=1, shape=(3, 3, 3))
        hc_nir = create_hypercube(name="nir", value=3, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[hc_red, hc_nir])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        udf_request = base64.b64encode(msgpack.packb(udf_request.dict(), use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request,
                                 headers={"Content-Type":"application/base64"})
        self.assertEqual(response.status_code, 200)
        blob = base64.b64decode(response.content)
        dict_data = msgpack.unpackb(blob, raw=False)

        self.checkHyperCubeNdvi(dict_data=dict_data)

    def checkHyperCubeNdvi(self, dict_data):
        """Check the ndvi hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc_ndvi: HyperCube = udata.hypercube_list[0]
        self.assertEqual(hc_ndvi.id, "NDVI")
        self.assertEqual(hc_ndvi.array.name, "NDVI")
        self.assertEqual(hc_ndvi.array.data.shape, (3, 3, 3))
        self.assertEqual(hc_ndvi.array.data[0][0][0], 0.5)
        self.assertEqual(hc_ndvi.array.data[2][2][2], 0.5)

    def checkHyperCubeMapFabs(self, dict_data):
        """Check the mapped fabs hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc_ndvi: HyperCube = udata.hypercube_list[0]
        self.assertEqual(hc_ndvi.id, "temp_fabs")
        self.assertEqual(hc_ndvi.array.name, "temp_fabs")
        self.assertEqual(hc_ndvi.array.data.shape, (3, 3, 3))
        self.assertEqual(hc_ndvi.array.data[0][0][0], 1)
        self.assertEqual(hc_ndvi.array.data[2][2][2], 1)

    def checkHyperCubeSum(self, dict_data):
        """Check the mean hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc: HyperCube = udata.hypercube_list[0]
        self.assertEqual(hc.id, "temp_sum")
        self.assertEqual(hc.array.name, "temp_sum")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 3)
        self.assertEqual(hc.array.data[2][2], 3)

    def checkHyperCubeMean(self, dict_data):
        """Check the mean hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc: HyperCube = udata.hypercube_list[0]
        self.assertEqual(hc.id, "temp_mean")
        self.assertEqual(hc.array.name, "temp_mean")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 1)
        self.assertEqual(hc.array.data[2][2], 1)

        hc: HyperCube = udata.hypercube_list[1]
        self.assertEqual(hc.id, "prec_mean")
        self.assertEqual(hc.array.name, "prec_mean")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 3)
        self.assertEqual(hc.array.data[2][2], 3)

    def checkHyperCubeMinMedianMax(self, dict_data):
        """Check the min, median, max hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc: HyperCube = udata.hypercube_list[0]
        self.assertEqual(hc.id, "temp_min")
        self.assertEqual(hc.array.name, "temp_min")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 1)
        self.assertEqual(hc.array.data[2][2], 1)

        hc: HyperCube = udata.hypercube_list[1]
        self.assertEqual(hc.id, "temp_median")
        self.assertEqual(hc.array.name, "temp_median")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 1)
        self.assertEqual(hc.array.data[2][2], 1)

        hc: HyperCube = udata.hypercube_list[2]
        self.assertEqual(hc.id, "temp_max")
        self.assertEqual(hc.array.name, "temp_max")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 1)
        self.assertEqual(hc.array.data[2][2], 1)


if __name__ == "__main__":
    unittest.main()
