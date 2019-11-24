# -*- coding: utf-8 -*-
import unittest
from openeo_udf.server.data_model.metadata_schema import MetadataModel
from openeo_udf.server.data_model.data_collection_schema import DataCollectionModel, ObjectCollectionModel, TimeStampsModel
from openeo_udf.server.data_model.model_example_creator import create_simple_feature_collection_model_example

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataCollectionModelWithSimpleFeaturesTest(unittest.TestCase):

    def test_data_cube_creation(self):
        m = MetadataModel(name="SimpleFeatureCollection",
                          description="New collection of simple features",
                          creator="Soeren",
                          creation_time="2001-01-01T10:00:00",
                          modification_time="2001-01-01T10:00:00",
                          number_of_object_collections=1,
                          number_of_geometries=3,
                          number_of_field_collections=1,
                          number_of_time_stamps=1)

        sfc, f_sfc, g = create_simple_feature_collection_model_example()

        oc = ObjectCollectionModel(data_cubes=[], simple_feature_collections=[sfc])

        ts = TimeStampsModel(calendar="gregorian", intervals=[("2001-01-01T10:00:00", "2001-01-01T00:02:00")])

        t = DataCollectionModel(metadata=m, object_collections=oc, geometry_collection=g,
                                variables_collections=[f_sfc], timestamps=ts)

        self.assertIsNotNone(t.json())
        print(t.json())
        print(t.schema_json())


if __name__ == '__main__':
    unittest.main()
