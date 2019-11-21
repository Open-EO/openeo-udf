"""
This module defines a number of function signatures that can be implemented by UDF's.
Both the name of the function and the argument types are/can be used by the backend to validate if the provided UDF
is compatible with the calling context of the process graph in which it is used.

"""


def open_file(file_identifier:str) :
    """
    Returns a local posix file path to a user resource. If needed, the backend will copy the user file to local disk.


    :param file_identifier:
    :return: a file handler
    """
    pass

from typing import Dict
def before_udf(context: Dict):
    """
    When a UDF implements this function, it will be executed at least once by the backend,
     before starting processing of the data.
    The implementation can extend the context dictionary, which will also be available when the udf is invoked.

    Backends are allowed to call the setup function multiple times, so the implementation should be idempotent.


    :param context: A dictionary object that should be initialized with user defined objects.
    :return:
    """
    pass

def after_udf(context:Dict):
    """
    Implement this process to clean up after running the UDF.
    :param context:
    :return:
    """
    pass



from pandas import Series
def apply_timeseries(series: Series,context:Dict)->Series:
    """
    Process a timeseries of values, without changing the time instants.
    This can for instance be used for smoothing or gap-filling.
    TODO: do we need geospatial coordinates for the series?

    :param series: A Pandas Series object with a date-time index.
    :param context: A dictionary containing user context.
    :return: A Pandas Series object with the same datetime index.
    """
    pass

from pandas import Series,DataFrame
from typing import Union
def reduce_timeseries(series:Union[Series,DataFrame],context):
    """
    Reduce a timeseries into a single value. If the input datacube has multiple bands, the series object will be a
    Dataframe, otherwise a Series.
    TODO: What about returning multiple values?

    :param series: A pandas Series or DataFrame object with a datetime index
    :return: A (single) value
    """
    pass


