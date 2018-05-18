# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
#import pandas
#import torch
#import torchvision
#import tensorflow
#import tensorboard
#from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile, UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def rct_time_sum(udf_data):
    """Reduce the time dimension for each tile and compute  sum for each pixel
    over time.

    Each raster tile in the udf data object will be reduced by time. Sum is
    computed for each pixel over time.

    Args:
        udf_data (UdfData): The UDF data object that contains raster tiles and vector data

    Returns:
        UdfData:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """

    # The list of tiles that were created
    tile_results = []

    # Iterate over each tile
    for tile in udf_data.raster_collection_tiles:
        tile_sum = numpy.sum(tile.data, axis=0)
        # We need to create a new 3D array with the correct shape for the computed aggregate
        rows, cols = tile_sum.shape
        array3d = numpy.ndarray([1, rows, cols])
        array3d[0] = tile_sum

        # Extract the start and end time to set the temporal extent for each tile
        starts = pandas.DatetimeIndex([tile.start_times[0]])
        ends = pandas.DatetimeIndex([tile.end_times[-1]])

        # Create the new raster collection tile
        rct = RasterCollectionTile(id=tile.id + "_sum", extent=tile.extent, data=array3d, start_times=starts,
                                   end_times=ends)
        tile_results.append(rct)

    udf_data.set_raster_collection_tiles(tile_results)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_time_sum(data)
