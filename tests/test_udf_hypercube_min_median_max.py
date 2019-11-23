# -*- coding: utf-8 -*-
import pprint
import os
import unittest
import msgpack
import base64

from openeo_udf.api.tools import create_hypercube
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


class HypercubeMinMedianMaxTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_hypercube_reduce_min_median_max(self):
        """Test the hypercube min, median, max reduction"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_reduce_time_min_median_max.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_hypercube(name="temp", value=1, dims=("t", "y", "x"), shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, hypercube_list=[temp])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()

        pprint.pprint(result)
        self.check_hyper_cube_min_median_max(dict_data=result)

    def check_hyper_cube_min_median_max(self, dict_data):
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
