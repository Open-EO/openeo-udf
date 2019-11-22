# -*- coding: utf-8 -*-

from openeo_udf.api.hypercube import HyperCube
from openeo_udf.api.udf_data import UdfData
from typing import Dict
import xarray

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def apply_hypercube(cube: HyperCube,context:Dict) -> HyperCube:
    """Compute the NDVI based on a hypercube

    A hypercube with a 'band' dimension is required. A 'red' and 'nir' band should be available.
    The NDVI computation will be applied to all hypercube dimensions.

    Args:
        cube (HyperCube): The hypercube object containing an xarray DaraArray

    Returns:
        a HyperCube containing the computed NDVI, the band dimension will be dropped.

    """
    array:xarray.DataArray = cube.get_array()
    red = array.sel(band='red')
    nir = array.sel(band='nir')

    ndvi = (nir - red) / (nir + red)
    ndvi.name = "NDVI"

    hc = HyperCube(array=ndvi)
    return hc

