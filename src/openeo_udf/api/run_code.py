# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""
from pprint import pprint

import xarray
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

from openeo_udf.api.feature_collection import FeatureCollection
from openeo_udf.api.datacube import DataCube
from openeo_udf.api.machine_learn_model import MachineLearnModel
from openeo_udf.api.spatial_extent import SpatialExtent
from openeo_udf.api.structured_data import StructuredData
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
    result_data = run_user_code(code, data)

    return result_data.to_dict()


def _build_default_execution_context():
    return {
        'numpy': numpy,
        'xarray': xarray,
        'geopandas': geopandas,
        'pandas': pandas,
        'shapely': shapely,
        'math':math,
        'FeatureCollection':FeatureCollection,
        'SpatialExtent':SpatialExtent,
        'StructuredData':StructuredData,
        'MachineLearnModel':MachineLearnModel,
        'torch':torch,
        'tensorflow':tensorflow,
        'DataCube':DataCube,
        'UdfData':UdfData
    }


def run_user_code(code:str, data:UdfData) -> UdfData:
    module={}
    exec(code, _build_default_execution_context(), module)

    functions = {t[0]:t[1] for t in module.items() if callable(t[1])}

    for func in functions.items():
        sig = signature(func[1])
        params = sig.parameters
        params_list = [t[1] for t in sig.parameters.items()]
        if(func[0] == 'apply_timeseries' and 'series' in params and 'context' in params and 'pandas.core.series.Series'
                in str(params['series'].annotation) and 'pandas.core.series.Series' in str(sig.return_annotation) ):
            #this is a UDF that transforms pandas series
            from .udf_wrapper import apply_timeseries_generic
            return apply_timeseries_generic(data, func[1])
        elif( func[0] == 'apply_hypercube' and 'cube' in params and 'context' in params and 'openeo_udf.api.datacube.DataCube'
              in str(params['cube'].annotation) and 'openeo_udf.api.datacube.DataCube' in str(sig.return_annotation) ):
            #found a datacube mapping function
            if len(data.get_datacube_list()) != 1:
                raise ValueError("The provided UDF expects exactly one datacube, but only: %s were provided." % len(data.get_datacube_list()))
            result_cube = func[1](data.get_datacube_list()[0], {})
            if not isinstance(result_cube,DataCube):
                raise ValueError("The provided UDF did not return a HyperCube, but got: %s" %result_cube)
            data.get_datacube_list([result_cube])
            break
        elif len(params_list) == 1 and (params_list[0].annotation == 'openeo_udf.api.udf_data.UdfData' or params_list[0].annotation == UdfData) :
            #found a generic UDF function
            func[1](data)
            break

    return data
