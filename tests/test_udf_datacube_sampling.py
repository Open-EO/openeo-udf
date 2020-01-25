# -*- coding: utf-8 -*-
import os
import unittest

from openeo_udf.api.run_code import run_user_code

from openeo_udf.api.tools import create_datacube
from openeo_udf.server.app import app
from starlette.testclient import TestClient
from openeo_udf.server.tools import create_storage_directory
from openeo_udf.server.data_model.udf_schemas import UdfCodeModel
from openeo_udf.api.udf_data import UdfData
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class HypercubeSamplingTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def not_implemented_yet_test_sampling(self):
        """Test the feature collection sampling UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "datacube_sampling.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_datacube(name="temp", value=1, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[temp])

        run_user_code(code=udf_code.source, data=udf_data)
        result = udf_data.to_dict()

        self.assertEqual(len(result["feature_collection_tiles"]), 1)
        self.assertEqual(len(result["feature_collection_tiles"][0]["data"]["features"]), 1)
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][0]["properties"], {'temp': 4})


if __name__ == "__main__":
    unittest.main()
