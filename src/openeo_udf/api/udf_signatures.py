"""
This module defines a number of function signatures that can be implemented by UDF's.
Both the name of the function and the argument types are/can be used by the backend to validate if the provided UDF
is compatible with the calling context of the process graph in which it is used.

"""
from pandas import Series,DataFrame
from typing import Union,Dict

from pandas import Series

from openeo_udf.api.datacube import DataCube


def apply_timeseries(series: Series,context:Dict)-> Series:
    """
    Process a timeseries of values, without changing the time instants.
    This can for instance be used for smoothing or gap-filling.
    TODO: do we need geospatial coordinates for the series?

    :param series: A Pandas Series object with a date-time index.
    :param context: A dictionary containing user context.
    :return: A Pandas Series object with the same datetime index.
    """
    pass




def apply_datacube(cube: DataCube,context:Dict)-> DataCube:
    """
    Map a DataCube to another DataCube. Depending on the context in which this function is used, the DataCube dimensions
    have to be retained or can be chained.
    For instance, in the context of a reducing operation along a dimension, that dimension will have to be reduced to a single value.
    In the context of a 1 to 1 mapping operation, all dimensions have to be retained.

    :param cube: A DataCube object
    :param context: A dictionary containing user context.
    :return: A DataCube object
    """
    pass
