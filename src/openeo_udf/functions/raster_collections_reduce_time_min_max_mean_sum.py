# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
#import pandas
#import torch
#import torchvision
#import tensorflow
#import tensorboard
from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile, UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def ict_min_mean_max_sum(udf_data: UdfData):
    """Reduce the time dimension for each tile and compute min, mean, max and sum for each pixel
    over time.

    Each raster tile in the udf data object will be reduced by time. Minimum, maximum, mean and sum are
    computed for each pixel over time.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    # The list of tiles that were created
    tile_results = []

    # Iterate over each tile
    for tile in udf_data.raster_collection_tiles:
        tile_min  = numpy.min(tile.data, axis=0)
        tile_max  = numpy.max(tile.data, axis=0)
        tile_sum  = numpy.sum(tile.data, axis=0)
        tile_mean = numpy.mean(tile.data, axis=0)
        # We need to create a new 3D array with the correct shape for each computed aggregate
        rows, cols = tile_sum.shape
        array3d_min  = numpy.ndarray(shape=[1, rows, cols])
        array3d_max  = numpy.ndarray([1, rows, cols])
        array3d_sum  = numpy.ndarray([1, rows, cols])
        array3d_mean = numpy.ndarray([1, rows, cols])
        array3d_min[0]  = tile_min
        array3d_max[0]  = tile_max
        array3d_sum[0]  = tile_sum
        array3d_mean[0] = tile_mean
        # Extract the start and end time to set the temporal extent for each tile
        if tile.start_times is not None and tile.end_times is not None:
            starts = pandas.DatetimeIndex([tile.start_times[0]])
            ends = pandas.DatetimeIndex([tile.end_times[-1]])
        else:
            starts = None
            ends = None
        # Create the new raster collection tiles
        rct = RasterCollectionTile(id=tile.id + "_min", extent=tile.extent, data=array3d_min,
                                   start_times=starts, end_times=ends)
        tile_results.append(rct)
        rct = RasterCollectionTile(id=tile.id + "_max", extent=tile.extent, data=array3d_max,
                                   start_times=starts, end_times=ends)
        tile_results.append(rct)
        rct = RasterCollectionTile(id=tile.id + "_sum", extent=tile.extent, data=array3d_sum,
                                   start_times=starts, end_times=ends)
        tile_results.append(rct)
        rct = RasterCollectionTile(id=tile.id + "_mean", extent=tile.extent, data=array3d_mean,
                                   start_times=starts, end_times=ends)
        tile_results.append(rct)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_raster_collection_tiles(tile_results)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
ict_min_mean_max_sum(data)
