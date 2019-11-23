#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

from typing import Tuple
import numpy
import xarray
from openeo_udf.api.datacube import DataCube

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


def create_datacube(name:str, value: float, shape: Tuple=(3, 2, 2), dims: Tuple=("t", "x", "y")) -> DataCube:
    """Create a datacube from shape and dimension parameter. The number of shapes and
    dimensions must be equal."""

    coords = {}
    for dim, size in zip(dims, shape):
        coords[dim] = list(range(size))

    array = xarray.DataArray(numpy.zeros(shape=shape), coords=coords, dims=dims)
    array.data += value
    array.name = name
    hc = DataCube(array=array)

    return hc

