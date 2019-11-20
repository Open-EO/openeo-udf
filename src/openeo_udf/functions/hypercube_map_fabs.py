# -*- coding: utf-8 -*-

from openeo_udf.api.hypercube import HyperCube
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def hyper_map_fabs(udf_data: UdfData):
    """Compute the absolute values of each hyper cube in the provided data

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
        result = numpy.fabs(cube.array)
        result.name = cube.id + "_fabs"
        cube_list.append(HyperCube(array=result))
    udf_data.set_hypercube_list(cube_list)


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
hyper_map_fabs(data)
