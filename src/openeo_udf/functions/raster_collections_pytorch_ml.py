# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
#import torch
#import torch.nn as nn
#import torch.nn.functional as F
#from torch.autograd import Variable
#import torch
#import torchvision
#import tensorflow
#import tensorboard
#from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile, UdfData, MachineLearnModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def rct_pytorch_ml(udf_data):
    """Apply a pre-trained pytorch machine learn model on the first tile

    The model must be a pytorch model that has expects the input data in the constructor
    The prediction method must accept a torch.autograd.Variable as input.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    tile = udf_data.raster_collection_tiles[0]

    # We need to reshape the data for prediction into one dimensional arrays
    three_dim_shape = tile.data.shape
    one_dim_shape = numpy.prod(three_dim_shape)

    tile_reshape = tile.data.reshape(one_dim_shape)

    # This is the input data of the model.
    input = Variable(torch.Tensor(tile_reshape))

    # Get the first model
    mlm = udf_data.get_ml_model_list()[0]
    m = mlm.get_model()
    # Predict the data
    pred = m(input)
    # Reshape the one dimensional predicted values to three dimensions based on the input shape
    pred_reshape = pred.reshape(three_dim_shape)

    # Create the new raster collection tile
    rct = RasterCollectionTile(id=mlm.name, extent=red.extent, data=pred_reshape,
                               start_times=red.start_times, end_times=red.end_times)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_raster_collection_tiles([rct,])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_pytorch_ml(data)
