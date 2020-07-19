# -*- coding: utf-8 -*-
import unittest
from openeo_udf.server.data_model.bounding_box_schema import SpatialBoundingBoxModel
from openeo_udf.server.data_model.simple_feature_collection_schema import SimpleFeatureModel, SimpleFeatureCollectionModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class SimpleFeatureTest(unittest.TestCase):

    def test_creation(self):

        bbox = SpatialBoundingBoxModel(min_x=0, max_x=1, min_y=0, max_y=0, min_z=0, max_z=0)

        sf = SimpleFeatureModel(type="LineString", geometry=0, field=[0, 0], timestamp=0, predecessors=[])
        sfc = SimpleFeatureCollectionModel(name="test",
                                           description="Simple features data A",
                                           number_of_features=1,
                                           features=[sf],
                                           bbox=bbox)

        self.assertIsNotNone(sfc.json())
        print(sfc.json())
        print(sfc.schema_json())


if __name__ == '__main__':
    unittest.main()
