# -*- coding: utf-8 -*-
import pprint
import os
import unittest

from openeo_udf.api.run_code import run_json_user_code, run_user_code

from openeo_udf.api.tools import create_datacube
from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfCodeModel, UdfRequestModel
from openeo_udf.api.udf_data import UdfData
from openeo_udf.api.datacube import DataCube
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class HypercubeSumTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_hypercube_reduce_sum(self):
        """Test the hypercube sum reduction"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "datacube_reduce_time_sum.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_datacube(name="temp", value=1, dims=("t", "x", "y"), shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[temp])

        run_user_code(udf_code=udf_code.source, udf_data=udf_data)
        self.checkHyperCubeSum(udf_data=udf_data)

    def checkHyperCubeSum(self, udf_data: UdfData):
        """Check the mean hyper cube data that was processed in the UDF server"""

        hc: DataCube = udf_data.datacube_list[0]
        self.assertEqual(hc.id, "temp_sum")
        self.assertEqual(hc.array.name, "temp_sum")
        self.assertEqual(hc.array.data.shape, (3, 3))
        self.assertEqual(hc.array.data[0][0], 3)
        self.assertEqual(hc.array.data[2][2], 3)


if __name__ == "__main__":
    unittest.main()
