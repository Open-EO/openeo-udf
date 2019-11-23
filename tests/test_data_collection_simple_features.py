# -*- coding: utf-8 -*-

import unittest

from openeo_udf.server.data_model.bounding_box_schema import SpatialBoundingBox
from openeo_udf.server.data_model.variables_collection_schema import Variable, VariablesCollection
from openeo_udf.server.data_model.metadata_schema import Metadata
from openeo_udf.server.data_model.simple_feature_collection_schema import SimpleFeature, SimpleFeatureCollection
from openeo_udf.server.data_model.data_collection_schema import DataCollection, ObjectCollection, TimeStamps

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class TopologicalDataCollectionTest(unittest.TestCase):

    def test_data_cube_creation(self):
        m = Metadata(name="SimpleFeatureCollection",
                     description="New collection of simple features",
                     creator="Soeren",
                     creation_time="2001-01-01T10:00:00",
                     modification_time="2001-01-01T10:00:00",
                     number_of_object_collections=1,
                     number_of_geometries=3,
                     number_of_field_collections=1,
                     number_of_time_stamps=1)

        g = ["LineString (2 0, 2 2)", "LineString (2 2, 0 1, 2 0)", "LineString (2 2, 3 1, 2 0)"]

        bbox = SpatialBoundingBox(min_x=0, max_x=3, min_y=0, max_y=2, min_z=0, max_z=0)

        sf1 = SimpleFeature(type="LineString", geometry=0, variable=[0, 0], timestamp=0, predecessors=[])
        sf2 = SimpleFeature(type="LineString", geometry=1, variable=[0, 0], timestamp=0, predecessors=[])
        sf3 = SimpleFeature(type="LineString", geometry=2, variable=[0, 0], timestamp=0, predecessors=[])
        sfs = SimpleFeatureCollection(name="Boundary of three lines",
                                      description="Boundary of three lines",
                                      number_of_features=3,
                                      features=[sf1, sf2, sf3],
                                      bbox=bbox,
                                      reference_system=4326)

        br = Variable(name="Landuse", description="Landuse", unit="category", values=[], labels=["Border"])

        f3 = VariablesCollection(name="Border", size=[1], number_of_variables=1, variables=[br])

        oc = ObjectCollection(data_cubes=[], simple_feature_collections=[sfs])

        ts = TimeStamps(calendar="gregorian", intervals=[("2001-01-01T10:00:00", "2001-01-01T00:02:00")])

        t = DataCollection(metadata=m, object_collections=oc, geometry_collection=g,
                           variables_collections=[f3], timestamps=ts)

        self.assertIsNotNone(t.json())
        print(t.json())
        print(t.schema_json())


if __name__ == '__main__':
    unittest.main()
