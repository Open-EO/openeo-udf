from openeo_udf.api.datacube import DataCube
from openeo_udf.api.udf_data import UdfData
from typing import Dict, Callable
import xarray
import numpy
import pandas
from pandas import Series


def apply_timeseries(series: Series, context:Dict)->Series:
    """
    Do something with the timeseries
    :param series:
    :param context:
    :return:
    """
    return series

def apply_timeseries_generic(udf_data: UdfData, callback: Callable = apply_timeseries):
    """
    Implements the UDF contract by calling a user provided time series transformation function (apply_timeseries).
    Multiple bands are currently handled separately, another approach could provide a dataframe with a timeseries for each band.

    :param udf_data:
    :return:
    """
    # The list of tiles that were created
    tile_results = []

    # Iterate over each cube
    for cube in udf_data.get_datacube_list():
        array3d = []
        #use rollaxis to make the time dimension the last one
        for time_x_slice in numpy.rollaxis(cube.array.values, 1):
            time_x_result = []
            for time_slice in time_x_slice:
                series = pandas.Series(time_slice)
                transformed_series = callback(series,udf_data.user_context)
                time_x_result.append(transformed_series)
            array3d.append(time_x_result)

        # We need to create a new 3D array with the correct shape for the computed aggregate
        result_tile = numpy.rollaxis(numpy.asarray(array3d),1)
        assert result_tile.shape == cube.array.shape
        # Create the new raster collection cube
        rct = DataCube(xarray.DataArray(result_tile))
        tile_results.append(rct)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_datacube_list(tile_results)
    return udf_data

