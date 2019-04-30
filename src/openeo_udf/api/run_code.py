# -*- coding: utf-8 -*-
import numpy
import pandas
import geopandas
import shapely
from copy import deepcopy
import torch
import torchvision
import tensorflow
import tensorboard
import math
from typing import Dict
from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile,\
    StructuredData, UdfData, HyperCube

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def run_json_user_code(json_data: Dict) -> Dict:
    """Run the user defined python code

    Args:
        json_data: the udf request object with code and data

    Returns:

    """
    code = json_data["code"]["source"]

    data = UdfData.from_dict(json_data["data"])

    exec(code)
    return data.to_dict()
