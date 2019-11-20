from openeo_udf.api.udf_data import UdfData,RasterCollectionTile
from typing import Dict

from pandas import Series
def apply_timeseries(series: Series,context:Dict)->Series:
    """
    Do something with the timeseries
    :param series:
    :param context:
    :return:
    """
    return series

import numpy
import pandas
def apply_timeseries_generic(udf_data: UdfData):
    # The list of tiles that were created
    tile_results = []

    # Iterate over each tile
    for tile in udf_data.raster_collection_tiles:
        array3d = []
        #use rollaxis to make the time dimension the last one
        for time_x_slice in numpy.rollaxis(tile.data, 1):
            time_x_result = []
            for time_slice in time_x_slice:
                series = pandas.Series(time_slice,index=tile.start_times)
                transformed_series = apply_timeseries(series,{})
                time_x_result.append(transformed_series)
            array3d.append(time_x_result)

        # We need to create a new 3D array with the correct shape for the computed aggregate
        result_tile = numpy.rollaxis(numpy.asarray(array3d),1)
        assert result_tile.shape == tile.data.shape
        # Create the new raster collection tile
        rct = RasterCollectionTile(id=tile.id, extent=tile.extent, data=result_tile,
                                   start_times=tile.start_times, end_times=tile.end_times)
        tile_results.append(rct)
    # Insert the new tiles as list of raster collection tiles in the input object. The new tiles will
    # replace the original input tiles.
    udf_data.set_raster_collection_tiles(tile_results)

