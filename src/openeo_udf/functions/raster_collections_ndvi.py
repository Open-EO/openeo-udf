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


def rct_ndvi(udf_data):
    """Compute the NDVI based on RED and NIR tiles

    Tiles with ids "red" and "nir" are required. The NDVI computation will be applied
    to all time stamped 2D raster tiles that have equal time stamps.

    Args:
        udf_data (UdfData): The UDF data object that contains raster tiles and vector data

    Returns:
        UdfData:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """

    red = None
    nir = None

    # Iterate over each tile
    for tile in udf_data.raster_collection_tiles:
        if "red" in tile.id.lower():

            red = tile
        if "nir" in tile.id.lower():
            nir = tile

    if red is None:
        raise Exception("Red raster collection tile is missing in input")

    if nir is None:
        raise Exception("Nir raster collection tile is missing in input")

    if red.start_times is None or red.start_times.tolist() == nir.start_times.tolist():

        ndvi = (nir.data - red.data) / (nir.data + red.data)

        # Create the new raster collection tile
        rct = RasterCollectionTile(id="ndvi", extent=red.extent, data=ndvi, start_times=red.start_times,
                                   end_times=red.end_times)

        udf_data.set_raster_collection_tiles([rct,])
    else:
        raise Exception("Time stamps are not equal")


rct_ndvi(data)
