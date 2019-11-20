# -*- coding: utf-8 -*-

import unittest

from openeo_udf.server.data_exchange_model.bounding_box import SpatialBoundingBox
from openeo_udf.server.data_exchange_model.field_collection import Field, FieldCollection
from openeo_udf.server.data_exchange_model.metadata import Metadata
from openeo_udf.server.data_exchange_model.simple_feature_collection import SimpleFeature, SimpleFeatureCollection
from openeo_udf.server.data_exchange_model.data_collection import DataCollection, CoordinateReferenceSystems, ObjectCollection

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

        crs = CoordinateReferenceSystems(EPSG=4326, temporal="gregorian")

        g = ["LineString (2 0, 2 2)", "LineString (2 2, 0 1, 2 0)", "LineString (2 2, 3 1, 2 0)"]

        bbox = SpatialBoundingBox(min_x=0, max_x=3, min_y=0, max_y=2, min_z=0, max_z=0)

        sf1 = SimpleFeature(type="LineString", geometry=0, field=[0, 0], timestamp=0, predecessors=[])
        sf2 = SimpleFeature(type="LineString", geometry=1, field=[0, 0], timestamp=0, predecessors=[])
        sf3 = SimpleFeature(type="LineString", geometry=2, field=[0, 0], timestamp=0, predecessors=[])
        sfs = SimpleFeatureCollection(name="Boundary of three lines",
                                      description="Boundary of three lines",
                                      number_of_features=3,
                                      features=[sf1, sf2, sf3],
                                      bbox=bbox)

        br = Field(name="Landuse", description="Landuse", unit="category", values=[], labels=["Border"])

        f3 = FieldCollection(name="Border", size=[1], number_of_fields=1, fields=[br])

        oc = ObjectCollection(data_cubes=[], simple_feature_collections=[sfs])

        ts = [("2001-01-01T10:00:00", None)]

        t = DataCollection(crs=crs, metadata=m, object_collections=oc, geometry_collection=g,
                                      field_collections=[f3], timestamps=ts)

        self.assertIsNotNone(t.json())
        print(t.json())
        print(t.schema_json())


if __name__ == '__main__':
    unittest.main()
