# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
#import pandas
#import torch
#import torchvision
#import tensorflow
#import tensorboard
from openeo_udf.api.hypercube import HyperCube
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def rct_ndvi(udf_data: UdfData):
    """Compute the NDVI based on RED and NIR hypercubes

    Hypercubes with ids "red" and "nir" are required. The NDVI computation will be applied
    to all hypercube dimensions.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles as well as hypercubes
        and structured data.

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    red = None
    nir = None

    # Iterate over each tile
    for cube in udf_data.get_hypercube_list():
        if "red" in cube.id.lower():
            red = cube
        if "nir" in cube.id.lower():
            nir = cube
    if red is None:
        raise Exception("Red hypercube is missing in input")
    if nir is None:
        raise Exception("Nir hypercube is missing in input")

    ndvi = (nir.array - red.array) / (nir.array + red.array)
    ndvi.name = "NDVI"

    hc = HyperCube(array=ndvi)
    udf_data.set_hypercube_list([hc, ])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_ndvi(data)
