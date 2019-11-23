# -*- coding: utf-8 -*-
import os
import unittest

from openeo_udf.api.tools import create_datacube
from openeo_udf.server.app import app
from starlette.testclient import TestClient
from openeo_udf.server.tools import create_storage_directory
from openeo_udf.server.data_model.udf_schemas import UdfCodeModel
from openeo_udf.api.udf_data import UdfData
from openeo_udf.api.datacube import DataCube
from openeo_udf.api.run_code import run_user_code
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
        run_user_code(udf_code=udf_code.source, udf_data=udf_data)
        self.checkHyperCubeMapFabs(udf_data=udf_data)

    def checkHyperCubeMapFabs(self, udf_data: UdfData):
        """Check the mapped fabs hyper cube data that was processed in the UDF server"""

        hc_ndvi: DataCube = udf_data.datacube_list[0]
        self.assertEqual(hc_ndvi.id, "temp_fabs")
        self.assertEqual(hc_ndvi.array.name, "temp_fabs")
        self.assertEqual(hc_ndvi.array.data.shape, (3, 3, 3))
        self.assertEqual(hc_ndvi.array.data[0][0][0], 1)
        self.assertEqual(hc_ndvi.array.data[2][2][2], 1)


if __name__ == "__main__":
    unittest.main()
