# -*- coding: utf-8 -*-

from openeo_udf.api.datacube import DataCube
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def hyper_mean(udf_data: UdfData):
    """Compute the mean of the time dimension of a hyper cube

    Hypercubes with time dimensions are required. The mean reduction of th time axis will be applied
    to all hypercube dimensions.

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles as well as hypercubes
        and structured data.

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    # Iterate over each tile
    cube_list = []
    for cube in udf_data.get_datacube_list():
        mean = cube.array.mean(dim="t")
        mean.name = cube.id + "_mean"
        cube_list.append(DataCube(array=mean))
    udf_data.set_datacube_list(cube_list)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
hyper_mean(data)
