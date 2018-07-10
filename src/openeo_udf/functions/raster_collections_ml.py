# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
#import pandas
#import torch
#import torchvision
#import tensorflow
#import tensorboard
#from sklearn.ensemble import RandomForestRegressor
#from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile, UdfData, MachineLearnModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def rct_ml(udf_data):
    """Apply a pre-trained machine learn model on RED and NIR tiles

    Tiles with ids "red" and "nir" are required. The machine learn model will be applied to all spatio-temporal pixel
    of the two input raster collections.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles

    Returns:
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

    # We need to reshape the data for prediction
    three_dim_shape = red.shape
    one_dim_shape = numpy.prod(three_dim_shape)

    red_reshape = red.data.reshape((one_dim_shape))
    nir_reshape = nir.data.reshape((one_dim_shape))
    X = [red_reshape, nir_reshape]
    # Get the first model
    mlm = data.get_ml_model_list()[0]
    m = mlm.get_model()
    pred = m.predict(X)
    pred_reshape = pred.reshape(three_dim_shape)

    # Create the new raster collection tile
    rct = RasterCollectionTile(id="ml", extent=red.extent, data=pred_reshape,
                               start_times=red.start_times, end_times=red.end_times)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_raster_collection_tiles([rct,])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_ml(data)
