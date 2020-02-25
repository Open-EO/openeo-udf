# -*- coding: utf-8 -*-

import unittest

from openeo_udf.server.data_model.datacube_schema import DataCubeModel, DimensionModel
from openeo_udf.server.data_model.variables_collection_schema import VariableModel, VariablesCollectionModel
from openeo_udf.server.data_model.metadata_schema import MetadataModel
from openeo_udf.server.data_model.data_collection_schema import DataCollectionModel, ObjectCollectionModel, \
    TimeStampsModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataCollectionTest(unittest.TestCase):

    def test_data_cube_creation(self):
        m = MetadataModel(name="Datacollection",
                          description="New collection",
                          creator="Soeren",
                          creation_time="2001-01-01T10:00:00",
                          modification_time="2001-01-01T10:00:00",
                          number_of_object_collections=1,
                          number_of_geometries=0,
                          number_of_field_collections=2,
                          number_of_time_stamps=1)

        # DATA CUBE

        dim_dict = {}
        dim_t = DimensionModel(description="Temporal dimension", type="temporal", reference_system="gregorian",
                               unit="ISO:8601",
                               values=["2001-01-01T00:00:00", "2001-01-01T00:01:00", "2001-01-01T00:02:00"],
                               extent=["2001-01-01T00:00:00", "2001-01-01T00:02:00"],
                               number_of_cells=3)
        dim_dict["time"] = dim_t
        dim_x = DimensionModel(description="Spatial dimension", type="spatial", reference_system=4326, axis="x",
                               unit="degree", values=[0, 1, 2, 3], extent=[0, 3],
                               number_of_cells=3)
        dim_dict["x"] = dim_x
        dim_y = DimensionModel(description="Spatial dimension", type="spatial", reference_system=4326, axis="y",
                               unit="degree", step=1, extent=[0, 3],
                               number_of_cells=3)
        dim_dict["y"] = dim_y

        dc = DataCubeModel(name="Data Cube", description="This is a data cube", dim=["time", "y", "x"], size=[3, 3, 3],
                           dimensions=dim_dict, field_collection=0, timestamp=0)

        # FIELD COLLECTION

        t = VariableModel(name="Temperature", description="Temperature", unit="degree celsius",
                          values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                  25, 26,
                                  27],
                          labels=[])

        p1 = VariableModel(name="Precipitation", description="Precipitation", unit="mm",
                           values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                   24, 25,
                                   26, 27],
                           labels=[])

        f1 = VariablesCollectionModel(name="Climate data", size=[3, 3, 3], number_of_variables=2, variables=[t, p1])

        # GEOMETRY COLLECTION

        g = []

        # OBJECT COLLECTION

        oc = ObjectCollectionModel(data_cubes=[dc], simple_feature_collections=[])

        ts = TimeStampsModel(calendar="gregorian", intervals=[("2001-01-01T10:00:00", "2001-01-01T00:02:00")])

        t = DataCollectionModel(metadata=m, object_collections=oc, geometry_collection=g,
                                variables_collections=[f1], timestamps=ts)

        self.assertIsNotNone(t.json())
        print(t.json())
        print(t.schema_json())


if __name__ == '__main__':
    unittest.main()
