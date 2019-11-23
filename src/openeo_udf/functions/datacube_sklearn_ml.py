# -*- coding: utf-8 -*-
import numpy
import pandas
import xarray

from openeo_udf.api.datacube import DataCube
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def rct_sklearn_ml(udf_data: UdfData):
    """Apply a pre-trained sklearn machine learn model on RED and NIR tiles

    The model must be a sklearn model that has a prediction method: m.predict(X)
    The prediction method must accept a pandas.DataFrame as input.

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

    # Iterate over each cube
    for cube in udf_data.get_datacube_list():
        if "red" in cube.id.lower():
            red = cube
        if "nir" in cube.id.lower():
            nir = cube
    if red is None:
        raise Exception("Red data cube is missing in input")
    if nir is None:
        raise Exception("Nir data cube is missing in input")

    # We need to reshape the data for prediction into one dimensional arrays
    three_dim_shape = red.array.shape
    one_dim_shape = numpy.prod(three_dim_shape)

    red_reshape = red.array.values.reshape((one_dim_shape))
    nir_reshape = nir.array.values.reshape((one_dim_shape))

    # This is the input data of the model. It must be trained with a DataFrame using the same names.
    X = pandas.DataFrame()
    X["red"] = red_reshape
    X["nir"] = nir_reshape

    # Get the first model
    mlm = udf_data.get_ml_model_list()[0]
    m = mlm.get_model()
    # Predict the data
    pred = m.predict(X)
    # Reshape the one dimensional predicted values to three dimensions based on the input shape
    pred_reshape = pred.reshape(three_dim_shape)

    result = xarray.DataArray(data=pred_reshape, dims=red.array.dims,
                              coords=red.array.coords, name=red.id + "_pytorch")
    # Create the new raster collection cube
    h = DataCube(array=result)
    # Insert the new hypercubes in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_datacube_list([h, ])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_sklearn_ml(data)
