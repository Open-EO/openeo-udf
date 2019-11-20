# -*- coding: utf-8 -*-

from openeo_udf.api.hypercube import HyperCube
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def hyper_min_median_max(udf_data: UdfData):
    """Compute the min, median and max of the time dimension of a hyper cube

    Hypercubes with time dimensions are required. The min, median and max reduction of th time axis will be applied
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
        min = cube.array.min(dim="time")
        median = cube.array.median(dim="time")
        max = cube.array.max(dim="time")

        min.name = cube.id + "_min"
        median.name = cube.id + "_median"
        max.name = cube.id + "_max"

        cube_list.append(HyperCube(array=min))
        cube_list.append(HyperCube(array=median))
        cube_list.append(HyperCube(array=max))

    udf_data.set_hypercube_list(cube_list)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
hyper_min_median_max(data)
