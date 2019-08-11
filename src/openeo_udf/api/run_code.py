# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

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

from openeo_udf.api.feature_collection_tile import FeatureCollectionTile
from openeo_udf.api.hypercube import HyperCube
from openeo_udf.api.machine_learn_model import MachineLearnModel
from openeo_udf.api.raster_collection_tile import RasterCollectionTile
from openeo_udf.api.spatial_extent import SpatialExtent
from openeo_udf.api.structured_data import StructuredData
from openeo_udf.api.custom_udf_parameter import CustomUdfParameter
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def run_json_user_code(dict_data: Dict) -> Dict:
    """Run the user defined python code

    Args:
        dict_data: the udf request object with code and data organized in a dictionary

    Returns:

    """
    code = dict_data["code"]["source"]

    data = UdfData.from_dict(dict_data["data"])

    exec(code)
    return data.to_dict()
