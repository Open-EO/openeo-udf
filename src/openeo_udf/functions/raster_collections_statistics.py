# -*- coding: utf-8 -*-
# Uncomment the import only for coding support
#import numpy
#import pandas
#import torch
#import torchvision
#import tensorflow
#import tensorboard

from openeo_udf.api.structured_data import StructuredData
from openeo_udf.api.udf_data import UdfData

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def rct_stats(udf_data: UdfData):
    """Compute univariate statistics for each raster collection tile

    Args:
        udf_data (UdfData): The UDF data object that contains raster and vector tiles

    Returns:
        This function will not return anything, the UdfData object "udf_data" must be used to store the resulting
        data.

    """
    # The dictionary that stores the statistical data
    stats = {}
    # Iterate over each raster collection tile and compute statistical values
    for tile in udf_data.raster_collection_tiles:
        # make sure to cast the values to floats, otherwise they are not serializable
        stats[tile.id] = dict(sum=float(tile.data.sum()), mean=float(tile.data.mean()),
                              min=float(tile.data.min()), max=float(tile.data.max()))
    # Create the structured data object
    sd = StructuredData(description="Statistical data sum, min, max and mean "
                                    "for each raster collection tile as dict",
                        data=stats,
                        type="dict")
    # Remove all collections and set the StructuredData list
    udf_data.del_raster_collection_tiles()
    udf_data.del_feature_collection_tiles()
    udf_data.set_structured_data_list([sd,])


# This function call is the entry point for the UDF.
# The caller will provide all required data in the **data** object.
rct_stats(data)
