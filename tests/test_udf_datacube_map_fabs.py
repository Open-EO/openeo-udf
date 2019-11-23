# -*- coding: utf-8 -*-
import pprint
import os
import unittest
import msgpack
import base64

from openeo_udf.api.tools import create_datacube
from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfCodeModel, UdfRequestModel
from openeo_udf.api.udf_data import UdfData
from openeo_udf.api.datacube import DataCube
from openeo_udf.api.run_code import run_json_user_code
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class HypercubeMapFabsTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_hypercube_map_fabs(self):
        """Test the hypercube mapping of the numpy fabs function"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "datacube_map_fabs.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_datacube(name="temp", value=1, dims=("t", "x", "y"), shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[temp])
        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)

        dict_data = run_json_user_code(dict_data=udf_request.dict())
        self.checkHyperCubeMapFabs(dict_data=dict_data)

    def checkHyperCubeMapFabs(self, dict_data):
        """Check the mapped fabs hyper cube data that was processed in the UDF server"""
        udata = UdfData.from_dict(dict_data)

        hc_ndvi: DataCube = udata.datacube_list[0]
        self.assertEqual(hc_ndvi.id, "temp_fabs")
        self.assertEqual(hc_ndvi.array.name, "temp_fabs")
        self.assertEqual(hc_ndvi.array.data.shape, (3, 3, 3))
        self.assertEqual(hc_ndvi.array.data[0][0][0], 1)
        self.assertEqual(hc_ndvi.array.data[2][2][2], 1)


if __name__ == "__main__":
    unittest.main()
