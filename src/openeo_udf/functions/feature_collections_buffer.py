# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
# import numpy
# import pandas
# import geopandas
# import torch
# import torchvision
# import tensorflow
# import tensorboard
# from shapely.geometry import Point

from openeo_udf.api.feature_collection import FeatureCollection
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def fct_buffer(udf_data: UdfData):
    """Compute buffer of size 10 around features

    This function creates buffer around all features in the provided feature collection tiles.
    The resulting geopandas.GeoDataFrame contains the new geometries and a copy of the original attribute data.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    fct_list = []

    # Iterate over each tile
    for tile in udf_data.feature_collection_list:
        # Buffer all features
        gseries = tile.data.buffer(distance=10)
        # Create a new GeoDataFrame that includes the buffered geometry and the attribute data
        new_data = tile.data.set_geometry(gseries)
        # Create the new feature collection tile
        fct = FeatureCollection(id=tile.id + "_buffer", data=new_data,
                                start_times=tile.start_times, end_times=tile.end_times)
        fct_list.append(fct)
    # Insert the new tiles as list of feature collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_feature_collection_list(fct_list)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
fct_buffer(data)

