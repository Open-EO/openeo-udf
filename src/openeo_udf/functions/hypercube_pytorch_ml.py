# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
import numpy
import xarray
import torch
import torchvision
import tensorflow
import tensorboard
from openeo_udf.api.hypercube import HyperCube

from openeo_udf.api.raster_collection_tile import RasterCollectionTile
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def hyper_pytorch_ml(udf_data: UdfData):
    """Apply a pre-trained pytorch machine learn model on a hypercube

    The model must be a pytorch model that has expects the input data in the constructor
    The prediction method must accept a torch.autograd.Variable as input.

    Args:
        udf_data (UdfData): The UDF data object that hypercubes and vector tiles

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    cube = udf_data.get_hypercube_list()[0]

    # This is the input data of the model.
    input = torch.autograd.Variable(torch.Tensor(cube.array.values))
    # Get the first model
    mlm = udf_data.get_ml_model_list()[0]
    m = mlm.get_model()
    # Predict the data
    pred = m(input)
    result = xarray.DataArray(data=pred.detach().numpy(), dims=cube.array.dims,
                              coords=cube.array.coords, name=cube.id + "_pytorch")
    # Create the new raster collection tile
    result_cube = HyperCube(array=result)
    # Insert the new  hypercube in the input object.
    udf_data.set_hypercube_list([result_cube])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
hyper_pytorch_ml(data)
