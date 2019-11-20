# -*- coding: utf-8 -*-

from openeo_udf.api.hypercube import HyperCube
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def hyper_sum(udf_data: UdfData):
    """Compute the sum of the time dimension of a hyper cube

    Hypercubes with time dimensions are required. The sum reduction of th time axis will be applied
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
    for cube in udf_data.get_hypercube_list():
        mean = cube.array.sum(dim="time")
        mean.name = cube.id + "_sum"
        cube_list.append(HyperCube(array=mean))
    udf_data.set_hypercube_list(cube_list)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
hyper_sum(data)
