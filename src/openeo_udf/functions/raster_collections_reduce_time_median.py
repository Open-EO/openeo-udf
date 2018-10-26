# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
import numpy
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


def rct_time_median(udf_data):
    """Reduce the time dimension for each tile and compute the median for each pixel
    over time.

    Each raster tile in the udf data object will be reduced by time. Median is
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
        tile_media = numpy.median(tile.data, axis=0)
        # We need to create a new 3D array with the correct shape for the computed aggregate
        rows, cols = tile_media.shape
        array3d = numpy.ndarray([1, rows, cols])
        array3d[0] = tile_media
        # Extract the start and end time to set the temporal extent for each tile
        if tile.start_times is not None and tile.end_times is not None:
            starts = pandas.DatetimeIndex([tile.start_times[0]])
            ends = pandas.DatetimeIndex([tile.end_times[-1]])
        else:
            starts = None
            ends = None
        # Create the new raster collection tile
        rct = RasterCollectionTile(id=tile.id + "_median", extent=tile.extent, data=array3d,
                                   start_times=starts, end_times=ends)
        tile_results.append(rct)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_raster_collection_tiles(tile_results)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_time_median(data)
