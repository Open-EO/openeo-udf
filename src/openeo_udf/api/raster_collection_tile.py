#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

import pandas
import numpy
from typing import Optional, Dict
from openeo_udf.api.spatial_extent import SpatialExtent
from openeo_udf.api.collection_tile import CollectionTile


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class RasterCollectionTile(CollectionTile):
    """This class represents a three dimensional raster collection tile with
    time information and x,y slices with a single scalar value for each pixel.
    A tile represents a scalar field in space and time,
    for example a time series of a single Landsat 8 or Sentinel2A band. A tile may be a
    spatio-temporal subset of a scalar time series or a whole time series.

    Some basic tests:

    >>> import numpy, pandas
    >>> data = numpy.zeros(shape=(1,1,1))
    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=100, width=100)
    >>> rct = RasterCollectionTile(id="test", extent=extent, data=data, wavelength=420)
    >>> rct.sample(50, 50)
    [0.0]
    >>> print(rct)
    id: test
    extent: top: 100
    bottom: 0
    right: 100
    left: 0
    height: 100
    width: 100
    wavelength: 420
    start_times: None
    end_times: None
    data: [[[0.]]]
    >>> dates = [pandas.Timestamp('2012-05-01')]
    >>> starts = pandas.DatetimeIndex(dates)
    >>> dates = [pandas.Timestamp('2012-05-02')]
    >>> ends = pandas.DatetimeIndex(dates)
    >>> rct = RasterCollectionTile(id="test", extent=extent,
    ...                            data=data, wavelength=420,
    ...                            start_times=starts, end_times=ends)
    >>> print(rct)
    id: test
    extent: top: 100
    bottom: 0
    right: 100
    left: 0
    height: 100
    width: 100
    wavelength: 420
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data: [[[0.]]]

    >>> import json
    >>> json.dumps(rct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"id": "test", "data": [[[0.0]]], "wavelength": 420, "start_times": ["2012-05-01T00:00:00"],
    "end_times": ["2012-05-02T00:00:00"],
    "extent": {"top": 100, "bottom": 0, "right": 100, "left": 0, "width": 100, "height": 100}}'


    >>> rct = RasterCollectionTile.from_dict(rct.to_dict())
    >>> json.dumps(rct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"id": "test", "data": [[[0.0]]], "wavelength": 420, "start_times": ["2012-05-01T00:00:00"],
    "end_times": ["2012-05-02T00:00:00"],
    "extent": {"top": 100, "bottom": 0, "right": 100, "left": 0, "width": 100, "height": 100}}'

    >>> data = numpy.zeros(shape=(3,10,10))
    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=10, width=10)
    >>> rct = RasterCollectionTile(id="test", extent=extent, data=data, wavelength=420)
    >>> rct.sample(50, 50)
    [0.0, 0.0, 0.0]


    >>> a = numpy.array([[[1., 2., 3., 4.],
    ...                   [5., 6., 7., 8.],
    ...                   [1., 2., 3., 4.]],
    ...                  [[5., 6., 7., 8.],
    ...                   [1., 2., 3., 4.],
    ...                   [5., 6., 7., 8.]]])
    >>>
    >>> extent = SpatialExtent(top=30, bottom=0, right=40, left=0, height=10, width=10)
    >>> rct = RasterCollectionTile(id="test", extent=extent, data=a, wavelength=420)
    >>> rct.sample(20, 15)
    [6.0, 2.0]
    >>> rct.sample(29, 1)
    [1.0, 5.0]
    >>> rct.sample(20, 21)
    [7.0, 3.0]
    >>> rct.sample(1, 39)
    [4.0, 8.0]

    """

    def __init__(self, id: str, extent: SpatialExtent, data: numpy.ndarray,
                 wavelength: Optional[float]=None,
                 start_times: Optional[pandas.DatetimeIndex]=None,
                 end_times: Optional[pandas.DatetimeIndex]=None):
        """Constructor of the tile of an raster collection

        Args:
            id (str): The unique id of the raster collection tile
            extent (SpatialExtent): The spatial extent with resolution information
            data (numpy.ndarray): The three dimensional numpy.ndarray with indices [t][y][x]
            wavelength (float): The optional wavelength of the raster collection tile
            start_times (pandas.DatetimeIndex): The vector with start times for each spatial x,y slice
            end_times (pandas.DatetimeIndex): The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals
        """

        CollectionTile.__init__(self, id=id, extent=extent, start_times=start_times, end_times=end_times)

        self.wavelength = wavelength
        self.set_data(data)
        self.check_data_with_time()

    def __str__(self) -> str:
        return "id: %(id)s\n" \
               "extent: %(extent)s\n" \
               "wavelength: %(wavelength)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s\n" \
               "data: %(data)s"%{"id":self.id, "extent":self.extent, "wavelength":self.wavelength,
                                 "start_times":self.start_times, "end_times":self.end_times, "data":self.data}

    def sample(self, top: float, left: float):
        """Sample the raster tile at specific top, left coordinates.

        If the coordinates are not in the spatial extent of the tile, then None will be returned.
        Otherwise a list of values, depending on the number of x,y slices are returned.

        The coordinates must be of the same projection as the raster collection.

        Args:
           top (float): The top (northern) coordinate of the point
           left (float): The left (western) coordinate of the point

        Returns:
            numpy.ndarray:
            A one dimensional array of values
        """
        if self.extent.contains_point(top=top, left=left) is True:
            x, y = self.extent.to_index(top, left)

            values = []
            for xy_slice in self.data:
                value = xy_slice[y][x]

                values.append(value)
            return values

        return None

    def get_data(self) -> numpy.ndarray:
        """Return the three dimensional numpy.ndarray with indices [t][y][x]

        Returns:
            numpy.ndarray: The three dimensional numpy.ndarray with indices [t][y][x]

        """
        return self._data

    def set_data(self, data: numpy.ndarray):
        """Set the three dimensional numpy.ndarray with indices [t][y][x]

        This function will check if the provided data is a numpy.ndarray with three dimensions

        Args:
            data (numpy.ndarray): The three dimensional numpy.ndarray with indices [t][y][x]

        """
        if isinstance(data, numpy.ndarray) is False:
            raise Exception("Argument data must be of type numpy.ndarray")

        if len(data.shape) != 3:
            raise Exception("Argument data must have three dimensions")

        self._data = data

    data = property(fget=get_data, fset=set_data)

    def to_dict(self) -> Dict:
        """Convert this RasterCollectionTile into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            RasterCollectionTile as a dictionary
        """

        d = {"id": self.id}
        if self._data is not None:
            d["data"] = self._data.tolist()
        if self.wavelength is not None:
            d["wavelength"] = self.wavelength
        if self._start_times is not None:
            d.update(self.start_times_to_dict())
        if self._end_times is not None:
            d.update(self.end_times_to_dict())
        if self._extent is not None:
            d.update(self.extent_to_dict())

        return d

    @staticmethod
    def from_dict(ict_dict: Dict):
        """Create a raster collection tile from a python dictionary that was created from
        the JSON definition of the RasterCollectionTile

        Args:
            ict_dict (dict): The dictionary that contains the raster collection tile definition

        Returns:
            RasterCollectionTile:
            A new RasterCollectionTile object

        """

        if "id" not in ict_dict:
            raise Exception("Missing id in dictionary")

        if "data" not in ict_dict:
            raise Exception("Missing data in dictionary")

        if "extent" not in ict_dict:
            raise Exception("Missing extent in dictionary")

        ict = RasterCollectionTile(id=ict_dict["id"],
                                   extent=SpatialExtent.from_dict(ict_dict["extent"]),
                                   data=numpy.asarray(ict_dict["data"]))

        if "start_times" in ict_dict:
            ict.set_start_times_from_list(ict_dict["start_times"])

        if "end_times" in ict_dict:
            ict.set_end_times_from_list(ict_dict["end_times"])

        if "wavelength" in ict_dict:
            ict.wavelength = ict_dict["wavelength"]

        return ict


if __name__ == "__main__":
    import doctest
    doctest.testmod()
