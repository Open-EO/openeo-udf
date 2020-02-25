# -*- coding: utf-8 -*-
import os
import unittest
import msgpack
import base64

from openeo_udf.api.run_code import run_user_code

from openeo_udf.api.tools import create_datacube
from openeo_udf.server.udf import app
from starlette.testclient import TestClient
from openeo_udf.server.tools import create_storage_directory
from openeo_udf.server.data_model.udf_schemas import UdfCodeModel, UdfRequestModel
from openeo_udf.api.udf_data import UdfData
from openeo_udf.api.datacube import DataCube
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataCubeNdviTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_DataCube_ndvi(self):
        """Test the DataCube NDVI computation"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "datacube_ndvi.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        hc_red = create_datacube(name="red", value=1, dims=("t", "y", "x"), shape=(3, 3, 3))
        hc_nir = create_datacube(name="nir", value=3, dims=("t", "y", "x"), shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[hc_red, hc_nir])

        run_user_code(code=udf_code.source, data=udf_data)
        self.checkDataCubeNdvi(udf_data=udf_data)

    def unused_test_DataCube_ndvi_message_pack(self):
        """Test the DataCube NDVI computation with the message pack protocol"""
        # TODO: Reactivate this test

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "datacube_ndvi.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        hc_red = create_datacube(name="red", value=1, dims=("t", "y", "x"), shape=(3, 3, 3))
        hc_nir = create_datacube(name="nir", value=3, dims=("t", "y", "x"), shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[hc_red, hc_nir])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        udf_request = base64.b64encode(msgpack.packb(udf_request.dict(), use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request,
                                 headers={"Content-Type": "application/base64"})
        self.assertEqual(response.status_code, 200)
        blob = base64.b64decode(response.content)
        udf_data = msgpack.unpackb(blob, raw=False)

        self.checkDataCubeNdvi(udf_data=udf_data)

    def checkDataCubeNdvi(self, udf_data:UdfData):
        """Check the ndvi hyper cube data that was processed in the UDF server"""

        hc_ndvi: DataCube = udf_data.datacube_list[0]
        self.assertEqual(hc_ndvi.id, "NDVI")
        self.assertEqual(hc_ndvi.array.name, "NDVI")
        self.assertEqual(hc_ndvi.array.data.shape, (3, 3, 3))
        self.assertEqual(hc_ndvi.array.data[0][0][0], 0.5)
        self.assertEqual(hc_ndvi.array.data[2][2][2], 0.5)


if __name__ == "__main__":
    unittest.main()
