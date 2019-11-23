# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
# import numpy
# import pandas
# import geopandas
# import torch
# import torchvision
# import tensorflow
# import tensorboard
# import math
# from shapely.geometry import Point

from openeo_udf.api.feature_collection import FeatureCollection
from openeo_udf.api.udf_data import UdfData
# from pprint import pprint

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def fct_sampling(udf_data: UdfData):
    """Sample any number of raster collection tiles with a single feature collection (the first if several are provided)
    and store the samples values in the input feature collection. Each time-slice of a raster collection is
    stored as a separate column in the feature collection. Hence, the size of the feature collection attributes
    is (number_of_raster_tile * number_of_xy_slices) x number_of_features.
    The number of columns is equal to (number_of_raster_tile * number_of_xy_slices).

    A single feature collection id stored in the input data object that contains the sample attributes and
    the original data.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """

    if not udf_data.feature_collection_list:
        raise Exception("A single feature collection is required as input")

    if len(udf_data.feature_collection_list) > 1:
        raise Exception("The first feature collection will be used for sampling")

    # Get the first feature collection
    fct = udf_data.feature_collection_list[0]
    features = fct.data

    # Iterate over each raster cube
    for cube in udf_data.get_datacube_list():

        # Compute the number and names of the attribute columns
        num_slices = len(cube.data)
        columns = {}
        column_names = []
        for slice in range(num_slices):
            column_name = cube.id + "_%i"%slice
            column_names.append(column_name)
            columns[column_name] = []

        # Sample the raster data with each point
        for feature in features.geometry:
            # Check if the feature is a point
            if feature.type == 'Point':
                x = feature.x
                y = feature.y
                # TODO: Thats needs to be implemented
                # values = cube.sample(top=y, left=x)

                values = [0, 0, 0]

                # Store the values in column specific arrays
                if values:
                    for column_name, value in zip(column_names, values):
                        columns[column_name].append(value)
                else:
                    for column_name in column_names:
                        columns[column_name].append(math.nan)
            else:
                raise Exception("Only points are allowed for sampling")
        # Attach the sampled attribute data to the GeoDataFrame
        for column_name in column_names:
            features[column_name] = columns[column_name]
    # Create the output feature collection
    fct = FeatureCollection(id=fct.id + "_sample", data=features,
                            start_times=fct.start_times, end_times=fct.end_times)
    # Insert the new tiles as list of feature collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_feature_collection_list([fct, ])
    # Remove the raster collection tiles
    udf_data.set_datacube_list()


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
fct_sampling(data)

