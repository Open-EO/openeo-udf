# -*- coding: utf-8 -*-
import unittest
import xarray
import numpy

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

        dcm = create_data_collection_model_example()
        dc = DataCube.from_data_collection(data_collection=dcm)
        print(dc[0].get_array())
        print(dc[1].get_array())

        dc1: DataCube = dc[0]
        dc2: DataCube = dc[1]

        self.assertEqual(dc1.id, dcm.variables_collections[0].variables[0].name)
        self.assertEqual(dc2.id, dcm.variables_collections[0].variables[1].name)

        a1: xarray.DataArray = dc1.get_array()
        a1 = numpy.asarray(a1).reshape([27])
        v1 = dcm.variables_collections[0].variables[0].values
        v1 = numpy.asarray(v1)
        self.assertTrue(a1.all() == v1.all())

        a2: xarray.DataArray = dc2.get_array()
        a2 = numpy.asarray(a2).reshape([27])
        v2 = dcm.variables_collections[0].variables[1].values
        v2 = numpy.asarray(v2)
        self.assertTrue(a2.all() == v2.all())




if __name__ == "__main__":
    unittest.main()
