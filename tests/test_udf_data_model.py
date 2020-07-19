# -*- coding: utf-8 -*-

import unittest
from openeo_udf.server.data_model.model_example_creator import create_udf_data_model_example

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfDataModelTest(unittest.TestCase):

    def test_udf_data_model_creation(self):

       udf_data = create_udf_data_model_example()

       self.assertIsNotNone(udf_data.json())
       print(udf_data.json())
       print(udf_data.schema_json())
