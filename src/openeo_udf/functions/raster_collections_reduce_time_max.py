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
    tile_results = []
    for tile in udf_data.raster_collection_tiles:
        tile_sum = numpy.sum(tile.data, axis=0)
        rows, cols = tile_sum.shape
        array3d = numpy.ndarray([1, rows, cols])
        array3d[0] = tile_sum

        starts = pandas.DatetimeIndex([tile.start_times[0]])
        ends = pandas.DatetimeIndex([tile.end_times[-1]])

        rct = RasterCollectionTile(id=tile.id + "_sum", extent=tile.extent, data=array3d, start_times=starts,
                                   end_times=ends)
        tile_results.append(rct)
    udf_data.set_raster_collection_tiles(tile_results)


rct_time_sum(data)
