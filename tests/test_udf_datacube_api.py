# -*- coding: utf-8 -*-
import unittest

from openeo_udf.server.app import app
from starlette.testclient import TestClient

from openeo_udf.server.data_model.model_example_creator import create_data_collection_model_example
from openeo_udf.server.tools import create_storage_directory
from openeo_udf.api.datacube import DataCube

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataCubeApiTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_hypercube_api(self):
        """Test the hypercube mean reduction"""

        dc = create_data_collection_model_example()
        dc = DataCube.from_data_collection(data_collection=dc, model_index=0)
        print(dc[0].get_array())
        print(dc[1].get_array())


if __name__ == "__main__":
    unittest.main()
