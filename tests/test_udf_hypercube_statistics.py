# -*- coding: utf-8 -*-
import pprint
import os
import unittest

from openeo_udf.api.run_code import run_json_user_code

from openeo_udf.api.tools import create_datacube
from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfCodeModel, UdfRequestModel
from openeo_udf.api.udf_data import UdfData
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class HypercubeStatisticsTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_rct_stats(self):
        """Test the raster collection tile statistics UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "datacube_statistics.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_datacube(name="temp", value=1, dims=("t", "x", "y"), shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[temp])

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        result = run_json_user_code(dict_data=udf_request.dict())

        self.assertEqual(len(result["datacubes"]), 0)
        self.assertEqual(len(result["structured_data_list"]), 1)
        self.assertEqual(result["structured_data_list"][0]["type"], "dict")
        self.assertEqual(result["structured_data_list"][0]["data"]["temp"], {'max': 1.0, 'mean': 1.0,
                                                                             'min': 1.0, 'sum': 27.0})


if __name__ == "__main__":
    unittest.main()
