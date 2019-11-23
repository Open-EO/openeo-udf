#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

import geopandas
import pandas
import json
from typing import Optional, Dict
from openeo_udf.api.collection_tile import CollectionBase


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class FeatureCollection(CollectionBase):
    """A feature collection  that represents a subset or a whole feature collection
    where single vector features may have time stamps assigned.

    Some basic tests:

    >>> from shapely.geometry import Point
    >>> import geopandas
    >>> p1 = Point(0,0)
    >>> p2 = Point(100,100)
    >>> p3 = Point(100,0)
    >>> pseries = [p1, p2, p3]
    >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
    >>> data["a"] = [1,2,3]
    >>> data["b"] = ["a","b","c"]
    >>> fct = FeatureCollection(id="test", data=data)
    >>> print(fct)
    id: test
    start_times: None
    end_times: None
    data:    a  b         geometry
    0  1  a      POINT (0 0)
    1  2  b  POINT (100 100)
    2  3  c    POINT (100 0)
    >>> import json
    >>> json.dumps(fct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"id": "test", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature",
    "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}},
    {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point",
    "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"},
    "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}'

    >>> p1 = Point(0,0)
    >>> pseries = [p1]
    >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
    >>> data["a"] = [1]
    >>> data["b"] = ["a"]
    >>> dates = [pandas.Timestamp('2012-05-01')]
    >>> starts = pandas.DatetimeIndex(dates)
    >>> dates = [pandas.Timestamp('2012-05-02')]
    >>> ends = pandas.DatetimeIndex(dates)
    >>> fct = FeatureCollection(id="test", start_times=starts, end_times=ends, data=data)
    >>> print(fct)
    id: test
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data:    a  b     geometry
    0  1  a  POINT (0 0)

    >>> import json
    >>> json.dumps(fct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"id": "test", "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"],
    "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature",
    "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}]}}'

    >>> fct = FeatureCollection.from_dict(fct.to_dict())
    >>> json.dumps(fct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"id": "test", "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"],
    "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature",
    "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}]}}'

    """

    def __init__(self, id: str, data: geopandas.GeoDataFrame,
                 start_times: Optional[pandas.DatetimeIndex]=None,
                 end_times: Optional[pandas.DatetimeIndex]=None):
        """Constructor of the  of a vector collection

        Args:
            id (str): The unique id of the vector collection
            data (geopandas.GeoDataFrame): A GeoDataFrame with geometry column and attribute data
            start_times (pandas.DateTimeIndex): The vector with start times for each spatial x,y slice
            end_times (pandas.DateTimeIndex): The pandas.DateTimeIndex vector with end times
                                              for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals
        """
        CollectionBase.__init__(self, id=id, start_times=start_times, end_times=end_times)

        self.set_data(data)
        self.check_data_with_time()

    def __str__(self):
        return "id: %(id)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s\n" \
               "data: %(data)s"%{"id":self.id, "extent":self.extent,
                                 "start_times":self.start_times,
                                 "end_times":self.end_times, "data":self.data}

    def get_data(self) -> geopandas.GeoDataFrame:
        """Return the geopandas.GeoDataFrame that contains the geometry column and any number of attribute columns

        Returns:
            geopandas.GeoDataFrame: A data frame that contains the geometry column and any number of attribute columns

        """
        return self._data

    def set_data(self, data: geopandas.GeoDataFrame):
        """Set the geopandas.GeoDataFrame that contains the geometry column and any number of attribute columns

        This function will check if the provided data is a geopandas.GeoDataFrame and raises
        an Exception

        Args:
            data (geopandas.GeoDataFrame): A GeoDataFrame with geometry column and attribute data

        """
        if isinstance(data, geopandas.GeoDataFrame) is False:
            raise Exception("Argument data must be of type geopandas.GeoDataFrame")

        self._data = data

    data = property(fget=get_data, fset=set_data)

    def to_dict(self) -> Dict:
        """Convert this FeatureCollection into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            FeatureCollection as a dictionary
        """

        d = {"id": self.id}
        if self._start_times is not None:
            d.update(self.start_times_to_dict())
        if self._end_times is not None:
            d.update(self.end_times_to_dict())
        if self._data is not None:
            d["data"] = json.loads(self._data.to_json())

        return d

    @staticmethod
    def from_dict(fct_dict: Dict):
        """Create a feature collection  from a python dictionary that was created from
        the JSON definition of the FeatureCollection

        Args:
            fct_dict (dict): The dictionary that contains the feature collection  definition

        Returns:
            FeatureCollection:
            A new FeatureCollection object

        """

        if "id" not in fct_dict:
            raise Exception("Missing id in dictionary")

        if "data" not in fct_dict:
            raise Exception("Missing data in dictionary")

        fct = FeatureCollection(id =fct_dict["id"],
                                data=geopandas.GeoDataFrame.from_features(fct_dict["data"]))

        if "start_times" in fct_dict:
            fct.set_start_times_from_list(fct_dict["start_times"])

        if "end_times" in fct_dict:
            fct.set_end_times_from_list(fct_dict["end_times"])

        return fct


if __name__ == "__main__":
    import doctest
    doctest.testmod()
