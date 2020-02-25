# -*- coding: utf-8 -*-

import unittest

from openeo_udf.server.data_model.model_example_creator import create_data_collection_model_example

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataCollectionTest(unittest.TestCase):

    def test_data_cube_creation(self):

        t = create_data_collection_model_example()

        self.assertIsNotNone(t.json())
        print(t.json())
        print(t.schema_json())


if __name__ == '__main__':
    unittest.main()
