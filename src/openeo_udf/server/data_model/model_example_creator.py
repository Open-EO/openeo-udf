# -*- coding: utf-8 -*-
from typing import Tuple, List
from openeo_udf.server.data_model.bounding_box_schema import SpatialBoundingBoxModel
from openeo_udf.server.data_model.datacube_schema import DataCubeModel, DimensionModel
from openeo_udf.server.data_model.machine_learn_schema import MachineLearnModel
from openeo_udf.server.data_model.structured_data_schema import StructuredDataModel
from openeo_udf.server.data_model.udf_schemas import UdfDataModel
from openeo_udf.server.data_model.variables_collection_schema import VariableModel, VariablesCollectionModel
from openeo_udf.server.data_model.metadata_schema import MetadataModel
from openeo_udf.server.data_model.simple_feature_collection_schema import SimpleFeatureModel, \
    SimpleFeatureCollectionModel
from openeo_udf.server.data_model.data_collection_schema import DataCollectionModel, ObjectCollectionModel, \
    TimeStampsModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_variable_collection_model_example():

    t = VariableModel(name="Temperature", description="Temperature", unit="degree celsius",
                      values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                              26,
                              27],
                      labels=[])

    p1 = VariableModel(name="Precipitation", description="Precipitation", unit="mm",
                       values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                               25,
                               26, 27],
                       labels=[])

    vc = VariablesCollectionModel(name="Climate data", size=[3, 3, 3], number_of_variables=2, variables=[t, p1])

    return vc


def create_dimension_model_example():
    dim_model = {}
    dim_t = DimensionModel(description="Temporal dimension", type="temporal", reference_system="gregorian",
                           unit="ISO:8601",
                           values=["2001-01-01T00:00:00", "2001-01-01T00:01:00", "2001-01-01T00:02:00"],
                           extent=["2001-01-01T00:00:00", "2001-01-01T00:02:00"],
                           number_of_cells=3)
    dim_model["time"] = dim_t
    dim_x = DimensionModel(description="Spatial dimension", type="spatial", reference_system=4326, axis="x",
                           unit="degree", values=[3.5, 4.5, 5.5], extent=[0, 3],
                           number_of_cells=3)
    dim_model["x"] = dim_x
    dim_y = DimensionModel(description="Spatial dimension", type="spatial", reference_system=4326, axis="y",
                           unit="degree", step=1, extent=[0, 3],
                           number_of_cells=3)
    dim_model["y"] = dim_y

    return dim_model


def create_datacube_model_example() -> Tuple[DataCubeModel, VariablesCollectionModel]:

    dim_model = create_dimension_model_example()
    dc = DataCubeModel(name="Data Cube", description="This is a data cube", dim=["time", "y", "x"], size=[3, 3, 3],
                       dimensions=dim_model, variable_collection=0, timestamp=0)

    vc = create_variable_collection_model_example()

    return dc, vc


def create_simple_feature_collection_model_example() -> Tuple[SimpleFeatureCollectionModel,
                                                              VariablesCollectionModel, List[str]]:
    g = ["LineString (2 0, 2 2)", "LineString (2 2, 0 1, 2 0)", "LineString (2 2, 3 1, 2 0)"]

    bbox = SpatialBoundingBoxModel(min_x=0, max_x=3, min_y=0, max_y=2, min_z=0, max_z=0)

    sf1 = SimpleFeatureModel(type="LineString", geometry=0, variable=[0, 0], timestamp=0, predecessors=[])
    sf2 = SimpleFeatureModel(type="LineString", geometry=1, variable=[0, 0], timestamp=0, predecessors=[])
    sf3 = SimpleFeatureModel(type="LineString", geometry=2, variable=[0, 0], timestamp=0, predecessors=[])
    sfc = SimpleFeatureCollectionModel(name="Boundary of three lines",
                                       description="Boundary of three lines",
                                       number_of_features=3,
                                       features=[sf1, sf2, sf3],
                                       bbox=bbox,
                                       reference_system=4326)

    br = VariableModel(name="Landuse", description="Landuse", unit="category", values=[], labels=["Border"])

    vc = VariablesCollectionModel(name="Border", size=[1], number_of_variables=1, variables=[br])

    return sfc, vc, g


def create_metadata_model_example() -> MetadataModel:

    m = MetadataModel(name="SimpleFeatureCollection",
                      description="New collection of simple features",
                      creator="Soeren",
                      creation_time="2001-01-01T10:00:00",
                      modification_time="2001-01-01T10:00:00",
                      number_of_object_collections=2,
                      number_of_geometries=3,
                      number_of_variable_collections=2,
                      number_of_time_stamps=1)
    return m


def create_object_collection_model_example() -> ObjectCollectionModel:

    dc, f_dc = create_datacube_model_example()

    sfc, f_sfc, g = create_simple_feature_collection_model_example()

    oc = ObjectCollectionModel(data_cubes=[dc], simple_feature_collections=[sfc])

    return oc


def create_timestamp_model_example() -> TimeStampsModel:

    return TimeStampsModel(calendar="gregorian", intervals=[("2001-01-01T10:00:00", "2001-01-01T00:02:00")])


def create_data_collection_model_example() -> DataCollectionModel:

    m = create_metadata_model_example()

    dc, f_dc = create_datacube_model_example()

    sfc, f_sfc, g = create_simple_feature_collection_model_example()

    oc = ObjectCollectionModel(data_cubes=[dc], simple_feature_collections=[sfc])

    ts = create_timestamp_model_example()

    dcm = DataCollectionModel(metadata=m, object_collections=oc, geometry_collection=g,
                              variables_collections=[f_dc, f_sfc], timestamps=ts)

    return dcm


def create_machine_learn_model_example() -> MachineLearnModel:

    return MachineLearnModel(framework="pytorch", name="linear_model",
                             description="A pytorch model that adds two numbers in range of [1,1]",
                             path="/tmp/simple_linear_nn_pytorch.pt")


def create_structured_data_model_example() -> StructuredDataModel:

    sdm = StructuredDataModel(description="Output of a statistical analysis. The univariate analysis "
                                          "of multiple raster collection tiles. "
                                          "Each entry in the output dict/map contains "
                                          "min, mean and max of all pixels in a raster collection tile. The key "
                                          "is the id of the raster collection tile.",
                              data={"RED": {"min": 0, "max": 100, "mean": 50},
                                    "NIR": {"min": 0, "max": 100, "mean": 50}},
                              type="dict")
    return sdm


def create_udf_data_model_example() -> UdfDataModel:

    sdm = create_structured_data_model_example()
    ml = create_machine_learn_model_example()
    dc = create_data_collection_model_example()

    udf_data = UdfDataModel(data_collection=dc, structured_data_list=[sdm], machine_learn_models=[ml],
                            user_context={"key": "value"}, server_context={"key": "value"})

    return udf_data
