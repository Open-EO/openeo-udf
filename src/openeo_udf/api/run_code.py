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
from inspect import signature

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
    result_data = run_user_code(code,data)

    return result_data.to_dict()

def _build_default_execution_context():
    return {
        'numpy': numpy,
        'geopandas': geopandas,
        'pandas': pandas,
        'shapely': shapely,
        'math':math,
        'RasterCollectionTile':RasterCollectionTile,
        'FeatureCollectionTile':FeatureCollectionTile,
        'SpatialExtent':SpatialExtent,
        'StructuredData':StructuredData,
        'CustomUdfParameter':CustomUdfParameter,
        'MachineLearnModel':MachineLearnModel,
        'torch':torch,
        'tensorflow':tensorflow,
        'HyperCube':HyperCube
    }

def run_user_code(code:str,udf_data:UdfData) -> UdfData:
    module={}
    exec(code,_build_default_execution_context(),module)

    functions = {t[0]:t[1] for t in module.items() if callable(t[1])}

    for func in functions.items():
        sig = signature(func[1])
        params = sig.parameters
        params_list = [t[1] for t in sig.parameters.items()]
        if(func[0] == 'apply_timeseries' and 'series' in params and 'context' in params and params['series'].annotation == 'pandas.core.series.Series' and sig.return_annotation == 'pandas.core.series.Series'):
            #this is a UDF that transforms pandas series
            from .udf_wrapper import apply_timeseries_generic
            return apply_timeseries_generic(udf_data,func[1])
        elif len(params_list) == 1 and (params_list[0].annotation == 'openeo_udf.api.udf_data.UdfData' or params_list[0].annotation == UdfData) :
            #found a generic UDF function
            func[1](udf_data)
            break

    return udf_data
