# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
import torch
#import torchvision
#import tensorflow
#import tensorboard
from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile, UdfData, MachineLearnModel

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

    # This is the input data of the model.
    input = torch.autograd.Variable(torch.Tensor(tile.data))

    # Get the first model
    mlm = udf_data.get_ml_model_list()[0]
    m = mlm.get_model()
    # Predict the data
    pred = m(input)
    # Create the new raster collection tile
    rct = RasterCollectionTile(id=mlm.name, extent=tile.extent, data=numpy.array(pred.tolist()),
                               start_times=tile.start_times, end_times=tile.end_times)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_raster_collection_tiles([rct,])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_pytorch_ml(data)
