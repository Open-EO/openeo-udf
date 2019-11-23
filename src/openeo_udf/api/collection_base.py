#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

import pandas
from typing import Optional, List, Dict
from openeo_udf.api.spatial_extent import SpatialExtent


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class CollectionBase:
    """This is the base class for raster and vector collection tiles. It implements
    start time, end time and spatial extent handling.

    Some basic tests:

    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=10, width=10)
    >>> coll = CollectionBase(id="test", extent=extent)
    >>> print(coll)
    id: test
    extent: top: 100
    bottom: 0
    right: 100
    left: 0
    height: 10
    width: 10
    start_times: None
    end_times: None

    >>> import pandas
    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=10, width=10)
    >>> dates = [pandas.Timestamp('2012-05-01')]
    >>> starts = pandas.DatetimeIndex(dates)
    >>> dates = [pandas.Timestamp('2012-05-02')]
    >>> ends = pandas.DatetimeIndex(dates)
    >>> rdc = CollectionBase(id="test", extent=extent,
    ...                      start_times=starts, end_times=ends)
    >>> "extent" in rdc.extent_to_dict()
    True
    >>> rdc.extent_to_dict()["extent"]["left"] == 0
    True
    >>> rdc.extent_to_dict()["extent"]["right"] == 100
    True
    >>> rdc.extent_to_dict()["extent"]["top"] == 100
    True
    >>> rdc.extent_to_dict()["extent"]["bottom"] == 0
    True
    >>> rdc.extent_to_dict()["extent"]["height"] == 10
    True
    >>> rdc.extent_to_dict()["extent"]["width"] == 10
    True

    >>> import json
    >>> json.dumps(rdc.start_times_to_dict())
    '{"start_times": ["2012-05-01T00:00:00"]}'
    >>> json.dumps(rdc.end_times_to_dict())
    '{"end_times": ["2012-05-02T00:00:00"]}'

    >>> ct = CollectionBase(id="test")
    >>> ct.set_extent_from_dict({"top": 53, "bottom": 50, "right": 30, "left": 24, "height": 0.01, "width": 0.01})
    >>> ct.set_start_times_from_list(["2012-05-01T00:00:00"])
    >>> ct.set_end_times_from_list(["2012-05-02T00:00:00"])
    >>> print(ct)
    id: test
    extent: top: 53
    bottom: 50
    right: 30
    left: 24
    height: 0.01
    width: 0.01
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)

    """

    def __init__(self, id: str, extent: Optional[SpatialExtent]=None,
                 start_times: Optional[pandas.DatetimeIndex]=None,
                 end_times: Optional[pandas.DatetimeIndex]=None):
        """Constructor of the base class for tile of a collection

        Args:
            id: The unique id of the raster collection tile
            extent: The spatial extent with resolution information, must be of type SpatialExtent
            start_times: The pandas.DateTimeIndex vector with start times for each spatial x,y slice
            end_times: The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals

        """

        self.id = id
        self._extent: Optional[SpatialExtent] = None
        self._start_times: Optional[pandas.DatetimeIndex] = None
        self._end_times: Optional[pandas.DatetimeIndex] = None
        self._data: List = None

        self.set_extent(extent=extent)
        self.set_start_times(start_times=start_times)
        self.set_end_times(end_times=end_times)

    def check_data_with_time(self):
        """Check if the start and end date vectors have the same size as the data
        """

        if self._data is not None and self.start_times is not None:
            if len(self.start_times) != len(self._data):
                raise Exception("The size of the start times vector just be equal "
                                "to the size of data")

        if self._data is not None and self.end_times is not None:
            if len(self.end_times) != len(self._data):
                raise Exception("The size of the end times vector just be equal "
                                "to the size of data")

    def __str__(self) -> str:
        return "id: %(id)s\n" \
               "extent: %(extent)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s"%{"id":self.id,
                                             "extent":self.extent,
                                             "start_times":self.start_times,
                                             "end_times":self.end_times}

    def get_start_times(self) -> Optional[pandas.DatetimeIndex]:
        """Returns the start time vector

        Returns:
            pandas.DatetimeIndex: Start time vector

        """
        return self._start_times

    def set_start_times(self, start_times: Optional[pandas.DatetimeIndex]):
        """Set the start times vector

        Args:
            start_times (pandas.DatetimeIndex): The start times vector

        """
        if start_times is None:
            return

        if isinstance(start_times, pandas.DatetimeIndex) is False:
            raise Exception("The start times vector mus be of type pandas.DatetimeIndex")

        self._start_times = start_times

    def get_end_times(self) -> Optional[pandas.DatetimeIndex]:
        """Returns the end time vector

        Returns:
            pandas.DatetimeIndex: End time vector

        """
        return self._end_times

    def set_end_times(self, end_times: Optional[pandas.DatetimeIndex]):
        """Set the end times vector

        Args:
            end_times (pandas.DatetimeIndex): The  end times vector
        """
        if end_times is None:
            return

        if isinstance(end_times, pandas.DatetimeIndex) is False:
            raise Exception("The start times vector mus be of type pandas.DatetimeIndex")

        self._end_times = end_times

    def get_extent(self) -> SpatialExtent:
        """Return the spatial extent

        Returns:
            SpatialExtent: The spatial extent

        """
        return self._extent

    def set_extent(self, extent: SpatialExtent):
        """Set the spatial extent

        Args:
            extent (SpatialExtent): The spatial extent with resolution information, must be of type SpatialExtent
        """
        if extent is None:
            return

        if isinstance(extent, SpatialExtent) is False:
            raise Exception("extent mus be of type SpatialExtent")

        self._extent = extent

    start_times = property(fget=get_start_times, fset=set_start_times)
    end_times = property(fget=get_end_times, fset=set_end_times)
    extent = property(fget=get_extent, fset=set_extent)

    def extent_to_dict(self) -> Dict:
        """Convert the extent into a dictionary representation that can be converted to JSON

        Returns:
            dict:
            The spatial extent

        """
        return self._extent.to_dict()

    def start_times_to_dict(self) -> Dict:
        """Convert the start times vector into a dictionary representation that can be converted to JSON

        Returns:
            dict:
            The start times vector

        """
        return dict(start_times=[t.isoformat() for t in self._start_times])

    def end_times_to_dict(self) -> Dict:
        """Convert the end times vector into a dictionary representation that can be converted to JSON

        Returns:
            dict:
            The end times vector

        """
        return dict(end_times=[t.isoformat() for t in self._end_times])

    def set_extent_from_dict(self, extent: Dict):
        """Set the spatial extent from a dictionary

        Args:
            extent (dict): The dictionary with the layout of the JSON SpatialExtent definition
        """
        self.set_extent(SpatialExtent.from_dict(extent))

    def set_start_times_from_list(self, start_times: Dict):
        """Set the start times vector from a dictionary

        Args:
            start_times (dict): The dictionary with the layout of the JSON start times vector definition
        """
        self.set_start_times(pandas.DatetimeIndex(start_times))

    def set_end_times_from_list(self, end_times: Dict):
        """Set the end times vector from a dictionary

        Args:
            end_times (dict): The dictionary with the layout of the JSON end times vector definition
        """
        self.set_end_times(pandas.DatetimeIndex(end_times))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
