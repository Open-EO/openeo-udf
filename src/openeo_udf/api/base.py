#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes of the OpenEO Python UDF interface

"""
import geopandas
import pandas
import numpy
from shapely.geometry import Polygon
from flask import json

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class SpatialExtent(object):
    """The axis aligned spatial extent of a collection tile

    Some basic tests:

    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
    >>> print(extent)
    north: 100
    south: 0
    east: 100
    west: 0
    nsres: 10
    ewres: 10

    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0)
    >>> print(extent)
    north: 100
    south: 0
    east: 100
    west: 0
    nsres: None
    ewres: None
    >>> p = extent.as_polygon()
    >>> print(p)
    POLYGON ((0 100, 100 100, 100 0, 0 0, 0 100))

    >>> from shapely.wkt import loads
    >>> p = loads("POLYGON ((0 100, 100 100, 100 0, 0 0, 0 100))")
    >>> extent = SpatialExtent.from_polygon(p)
    >>> print(extent)
    north: 100.0
    south: 0.0
    east: 100.0
    west: 0.0
    nsres: None
    ewres: None
    
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0)
    >>> extent.as_polygon() == extent.as_polygon()
    True
    >>> diff = extent.as_polygon() - extent.as_polygon()
    >>> print(diff)
    GEOMETRYCOLLECTION EMPTY

    >>> extent_1 = SpatialExtent(north=80, south=10, east=80, west=10)
    >>> extent_2 = SpatialExtent(north=100, south=0, east=100, west=0)
    >>> extent_1.as_polygon() == extent_2.as_polygon()
    False
    >>> extent_2.as_polygon().contains(extent_2.as_polygon())
    True

    """

    def __init__(self, north, south, east, west, nsres=None, ewres=None):
        """Constructor of the axis aligned spatial extent of a collection tile

        Args:
            north (float): The northern border of the data chunk
            south (float): The southern border of the data chunk
            east (float): The eastern border of the data chunk
            west (float): The west border of the data chunk
            nsres (float): The north-south pixel resolution (ignored in case of vector data chunks)
            ewres (float): The east-west pixel resolution (ignored in case of vector data chunks)

        """

        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.nsres = nsres
        self.ewres = ewres

    def __str__(self):
        return "north: %(n)s\n" \
               "south: %(s)s\n" \
               "east: %(e)s\n" \
               "west: %(w)s\n" \
               "nsres: %(ns)s\n" \
               "ewres: %(ew)s"%{"n":self.north, "s":self.south, "e":self.east,
                                "w":self.west, "ns":self.nsres, "ew":self.ewres}

    def as_polygon(self):
        """Return the extent as shapely.geometry.Polygon to perform
        comparison operations between other extents like equal, intersect and so on

        Returns:
            shapely.geometry.Polygon: The polygon representing the spatial extent

        """

        return Polygon([(self.west, self.north),(self.east, self.north),
                        (self.east, self.south),(self.west, self.south)])

    @staticmethod
    def from_polygon(polygon):
        """Convert a polygon with rectangular shape into a spatial extent

        Args:
            polygon (shapely.geometry.Polygon): The polygon that should be converted into a spatial extent

        Returns:
            SpatialExtent: The spatial extent

        """

        coords = list(polygon.exterior.coords)

        north = coords[0][1]
        south = coords[2][1]
        east = coords[1][0]
        west = coords[0][0]

        return SpatialExtent(north=north, south=south, east=east, west=west)

    def to_dict(self):
        """Return the spatial extent as a dict that can be easily converted into JSON

        Returns:
            dict:
            Dictionary representation

        """
        d = dict(extent=dict(north=self.north, south=self.south, east=self.east,
                             west=self.west))

        if self.ewres:
            d["extent"].update({"ewres":self.ewres})
        if self.nsres:
            d["extent"].update({"nsres":self.nsres})

        return d

    @staticmethod
    def from_dict(extent):
        """Create a SpatialExtent from a python dictionary that was created from
        the JSON definition of the SpatialExtent

        Args:
            extent (dict): The dictionary that contains the spatial extent definition

        Returns:
            SpatialExtent:
            A new SpatialExtent object

        """

        north = None
        south = None
        east = None
        west = None
        ewres = None
        nsres = None

        if "north" in extent:
            north = extent["north"]
        if "south" in extent:
            south = extent["south"]
        if "east" in extent:
            east = extent["east"]
        if "west" in extent:
            west = extent["west"]
        if "ewres" in extent:
            ewres = extent["ewres"]
        if "nsres" in extent:
            nsres = extent["nsres"]

        return SpatialExtent(north=north, south=south, west=west, east=east, nsres=nsres, ewres=ewres)


class CollectionTile(object):
    """This is the base class for image and vector collection tiles. It implements
    start time, end time and spatial extent handling.

    Some basic tests:

    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
    >>> coll = CollectionTile(id="test", extent=extent)
    >>> print(coll)
    id: test
    extent: north: 100
    south: 0
    east: 100
    west: 0
    nsres: 10
    ewres: 10
    start_times: None
    end_times: None

    >>> import pandas
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
    >>> dates = [pandas.Timestamp('2012-05-01')]
    >>> starts = pandas.DatetimeIndex(dates)
    >>> dates = [pandas.Timestamp('2012-05-02')]
    >>> ends = pandas.DatetimeIndex(dates)
    >>> rdc = CollectionTile(id="test", extent=extent,
    ...                      start_times=starts, end_times=ends)
    >>> "extent" in rdc.extent_to_dict()
    True
    >>> rdc.extent_to_dict()["extent"]["west"] == 0
    True
    >>> rdc.extent_to_dict()["extent"]["east"] == 100
    True
    >>> rdc.extent_to_dict()["extent"]["north"] == 100
    True
    >>> rdc.extent_to_dict()["extent"]["south"] == 0
    True
    >>> rdc.extent_to_dict()["extent"]["nsres"] == 10
    True
    >>> rdc.extent_to_dict()["extent"]["ewres"] == 10
    True

    >>> from flask import json
    >>> json.dumps(rdc.start_times_to_dict())
    '{"start_times": ["2012-05-01T00:00:00"]}'
    >>> json.dumps(rdc.end_times_to_dict())
    '{"end_times": ["2012-05-02T00:00:00"]}'

    >>> ct = CollectionTile(id="test")
    >>> ct.set_extent_from_dict({"north": 53, "south": 50, "east": 30, "west": 24, "nsres": 0.01, "ewres": 0.01})
    >>> ct.set_start_times_from_list(["2012-05-01T00:00:00"])
    >>> ct.set_end_times_from_list(["2012-05-02T00:00:00"])
    >>> print(ct)
    id: test
    extent: north: 53
    south: 50
    east: 30
    west: 24
    nsres: 0.01
    ewres: 0.01
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)



    """

    def __init__(self, id, extent=None, start_times=None, end_times=None):
        """Constructor of the base class for tile of a collection

        Args:
            id: The unique id of the raster collection tile
            extent: The spatial extent with resolution information, must be of type SpatialExtent
            start_times: The pandas.DateTimeIndex vector with start times for each spatial x,y slice
            end_times: The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals

        """

        self.id = id
        self._extent = None
        self._start_times = None
        self._end_times = None
        self._data = None

        self.set_extent(extent=extent)
        self.set_start_times(start_times=start_times)
        self.set_end_times(end_times=end_times)

    def check_data_with_time(self):
        """Check if the start and end date vectors have the same size as the data
        """

        if self._data is not None and self.start_times is not None:
            if len(self.start_times) != len(self.data):
                raise Exception("The size of the start times vector just be equal "
                                "to the size of data")

        if self._data is not None and self.end_times is not None:
            if len(self.end_times) != len(self.data):
                raise Exception("The size of the end times vector just be equal "
                                "to the size of data")

    def __str__(self):
        return "id: %(id)s\n" \
               "extent: %(extent)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s"%{"id":self.id,
                                             "extent":self.extent,
                                             "start_times":self.start_times,
                                             "end_times":self.end_times}

    def get_start_times(self):
        """Returns the start time vector

        Returns:
            pandas.DatetimeIndex: Start time vector

        """
        return self._start_times

    def set_start_times(self, start_times):
        """Set the start times vector

        Args:
            start_times (pandas.DatetimeIndex): The start times vector

        """
        if start_times is None:
            return

        if isinstance(start_times, pandas.DatetimeIndex) is False:
            raise Exception("The start times vector mus be of type pandas.DatetimeIndex")

        self._start_times = start_times

    def get_end_times(self):
        """Returns the end time vector

        Returns:
            pandas.DatetimeIndex: End time vector

        """
        return self._end_times

    def set_end_times(self, end_times):
        """Set the end times vector

        Args:
            end_times (pandas.DatetimeIndex): The  end times vector
        """
        if end_times is None:
            return

        if isinstance(end_times, pandas.DatetimeIndex) is False:
            raise Exception("The start times vector mus be of type pandas.DatetimeIndex")

        self._end_times = end_times

    def get_extent(self):
        """Return the spatial extent

        Returns:
            SpatialExtent: The spatial extent

        """
        return self._extent

    def set_extent(self, extent):
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

    def extent_to_dict(self):
        """Convert the extent into a dictionary representation that can be converted to JSON

        Returns:
            dict:
            The spatial extent

        """
        return self._extent.to_dict()

    def start_times_to_dict(self):
        """Convert the start times vector into a dictionary representation that can be converted to JSON

        Returns:
            dict:
            The start times vector

        """
        return dict(start_times=[t.isoformat() for t in self._start_times])

    def end_times_to_dict(self):
        """Convert the end times vector into a dictionary representation that can be converted to JSON

        Returns:
            dict:
            The end times vector

        """
        return dict(end_times=[t.isoformat() for t in self._end_times])

    def set_extent_from_dict(self, extent):
        """Set the spatial extent from a dictionary

        Args:
            extent (dict): The dictionary with the layout of the JSON SpatialExtent definition
        """
        self.set_extent(SpatialExtent.from_dict(extent))

    def set_start_times_from_list(self, start_times):
        """Set the start times vector from a dictionary

        Args:
            start_times (dict): The dictionary with the layout of the JSON start times vector definition
        """
        self.set_start_times(pandas.DatetimeIndex(start_times))

    def set_end_times_from_list(self, end_times):
        """Set the end times vector from a dictionary

        Args:
            end_times (dict): The dictionary with the layout of the JSON end times vector definition
        """
        self.set_end_times(pandas.DatetimeIndex(end_times))


class RasterCollectionTile(CollectionTile):
    """This class represents a three dimensional raster collection tile with
    time information and x,y slices with a single scalar value for each pixel.
    A tile represents a scalar field in space and time,
    for example a time series of a single Landsat 8 or Sentinel2A band. A tile may be a
    spatio-temporal subset of a scalar time series or a whole time series.

    Some basic tests:

    >>> import numpy, pandas
    >>> data = numpy.zeros(shape=(1,1,1))
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
    >>> rct = RasterCollectionTile(id="test", extent=extent, data=data, wavelength=420)
    >>> print(rct)
    id: test
    extent: north: 100
    south: 0
    east: 100
    west: 0
    nsres: 10
    ewres: 10
    wavelength: 420
    start_times: None
    end_times: None
    data: [[[0.]]]
    >>> dates = [pandas.Timestamp('2012-05-01')]
    >>> starts = pandas.DatetimeIndex(dates)
    >>> dates = [pandas.Timestamp('2012-05-02')]
    >>> ends = pandas.DatetimeIndex(dates)
    >>> rct = RasterCollectionTile(id="test", extent=extent,
    ...                           data=data, wavelength=420,
    ...                           start_times=starts, end_times=ends)
    >>> print(rct)
    id: test
    extent: north: 100
    south: 0
    east: 100
    west: 0
    nsres: 10
    ewres: 10
    wavelength: 420
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data: [[[0.]]]

    >>> from flask import json
    >>> json.dumps(rct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"data": [[[0.0]]],
    "end_times": ["2012-05-02T00:00:00"],
    "extent": {"east": 100, "ewres": 10, "north": 100, "nsres": 10, "south": 0, "west": 0},
    "id": "test",
    "start_times": ["2012-05-01T00:00:00"],
    "wavelength": 420}'

    >>> rct = RasterCollectionTile.from_dict(rct.to_dict())
    >>> json.dumps(rct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"data": [[[0.0]]],
    "end_times": ["2012-05-02T00:00:00"],
    "extent": {"east": 100, "ewres": 10, "north": 100, "nsres": 10, "south": 0, "west": 0},
    "id": "test",
    "start_times": ["2012-05-01T00:00:00"],
    "wavelength": 420}'

    """

    def __init__(self, id, extent, data, wavelength=None, start_times=None, end_times=None):
        """Constructor of the tile of an raster collection

        Args:
            id (str): The unique id of the raster collection tile
            extent (SpatialExtent): The spatial extent with resolution information
            data (numpy.ndarray): The three dimensional numpy.ndarray with indices [t][y][x]
            wavelength (float): The optional wavelength of the raster collection tile
            start_times (pandas.DateTimeIndex): The vector with start times for each spatial x,y slice
            end_times (pandas.DateTimeIndex): The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals
        """

        CollectionTile.__init__(self, id=id, extent=extent, start_times=start_times, end_times=end_times)

        self.wavelength = wavelength
        self.set_data(data)
        self.check_data_with_time()

    def __str__(self):
        return "id: %(id)s\n" \
               "extent: %(extent)s\n" \
               "wavelength: %(wavelength)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s\n" \
               "data: %(data)s"%{"id":self.id, "extent":self.extent, "wavelength":self.wavelength,
                                   "start_times":self.start_times, "end_times":self.end_times, "data":self.data}

    def get_data(self):
        """Return the three dimensional numpy.ndarray with indices [t][y][x]

        Returns:
            numpy.ndarray: The three dimensional numpy.ndarray with indices [t][y][x]

        """
        return self._data

    def set_data(self, data):
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

    def to_dict(self):
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
    def from_dict(ict_dict):
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

        ict = RasterCollectionTile(id =ict_dict["id"],
                                   extent=SpatialExtent.from_dict(ict_dict["extent"]),
                                   data=numpy.asarray(ict_dict["data"]))

        if "start_times" in ict_dict:
            ict.set_start_times_from_list(ict_dict["start_times"])

        if "end_times" in ict_dict:
            ict.set_end_times_from_list(ict_dict["end_times"])

        if "wavelength" in ict_dict:
            ict.wavelength = ict_dict["wavelength"]

        return ict


class FeatureCollectionTile(CollectionTile):
    """A feature collection tile that represents a subset or a whole feature collection
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
    >>> fct = FeatureCollectionTile(id="test", data=data)
    >>> print(fct)
    id: test
    start_times: None
    end_times: None
    data:    a  b         geometry
    0  1  a      POINT (0 0)
    1  2  b  POINT (100 100)
    2  3  c    POINT (100 0)
    >>> from flask import json
    >>> json.dumps(fct.to_dict())
    '{"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"}, "id": "0", "properties": {"a": 1, "b": "a"}, "type": "Feature"}, {"geometry": {"coordinates": [100.0, 100.0], "type": "Point"}, "id": "1", "properties": {"a": 2, "b": "b"}, "type": "Feature"}, {"geometry": {"coordinates": [100.0, 0.0], "type": "Point"}, "id": "2", "properties": {"a": 3, "b": "c"}, "type": "Feature"}], "type": "FeatureCollection"}, "id": "test"}'

    >>> p1 = Point(0,0)
    >>> pseries = [p1]
    >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
    >>> data["a"] = [1]
    >>> data["b"] = ["a"]
    >>> dates = [pandas.Timestamp('2012-05-01')]
    >>> starts = pandas.DatetimeIndex(dates)
    >>> dates = [pandas.Timestamp('2012-05-02')]
    >>> ends = pandas.DatetimeIndex(dates)
    >>> fct = FeatureCollectionTile(id="test", start_times=starts, end_times=ends, data=data)
    >>> print(fct)
    id: test
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data:    a  b     geometry
    0  1  a  POINT (0 0)

    >>> from flask import json
    >>> json.dumps(fct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"}, "id": "0",
                             "properties": {"a": 1, "b": "a"}, "type": "Feature"}],
               "type": "FeatureCollection"},
    "end_times": ["2012-05-02T00:00:00"],
    "id": "test",
    "start_times": ["2012-05-01T00:00:00"]}'

    >>> fct = FeatureCollectionTile.from_dict(fct.to_dict())
    >>> json.dumps(fct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"}, "id": "0",
                             "properties": {"a": 1, "b": "a"}, "type": "Feature"}],
               "type": "FeatureCollection"},
    "end_times": ["2012-05-02T00:00:00"],
    "id": "test",
    "start_times": ["2012-05-01T00:00:00"]}'

    """

    def __init__(self, id, data, start_times=None, end_times=None):
        """Constructor of the tile of a vector collection

        Args:
            id (str): The unique id of the vector collection tile
            data (geopandas.GeoDataFrame): A GeoDataFrame with geometry column and attribute data
            start_times (pandas.DateTimeIndex): The vector with start times for each spatial x,y slice
            end_times (pandas.DateTimeIndex): The pandas.DateTimeIndex vector with end times
                                              for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals
        """
        CollectionTile.__init__(self, id=id, start_times=start_times, end_times=end_times)

        self.set_data(data)
        self.check_data_with_time()

    def __str__(self):
        return "id: %(id)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s\n" \
               "data: %(data)s"%{"id":self.id, "extent":self.extent,
                                 "start_times":self.start_times,
                                 "end_times":self.end_times, "data":self.data}

    def get_data(self):
        """Return the geopandas.GeoDataFrame that contains the geometry column and any number of attribute columns

        Returns:
            geopandas.GeoDataFrame: A data frame that contains the geometry column and any number of attribute columns

        """
        return self._data

    def set_data(self, data):
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

    def to_dict(self):
        """Convert this FeatureCollectionTile into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            FeatureCollectionTile as a dictionary
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
    def from_dict(fct_dict):
        """Create a feature collection tile from a python dictionary that was created from
        the JSON definition of the FeatureCollectionTile

        Args:
            fct_dict (dict): The dictionary that contains the feature collection tile definition

        Returns:
            FeatureCollectionTile:
            A new FeatureCollectionTile object

        """

        if "id" not in fct_dict:
            raise Exception("Missing id in dictionary")

        if "data" not in fct_dict:
            raise Exception("Missing data in dictionary")

        fct = FeatureCollectionTile(id =fct_dict["id"],
                                    data=geopandas.GeoDataFrame.from_features(fct_dict["data"]))

        if "start_times" in fct_dict:
            fct.set_start_times_from_list(fct_dict["start_times"])

        if "end_times" in fct_dict:
            fct.set_end_times_from_list(fct_dict["end_times"])

        return fct


class UdfData(object):
    """The class that stores the arguments for a user defined function (UDF)

    Some basic tests:

    >>> from shapely.geometry import Point
    >>> import geopandas
    >>> import numpy, pandas
    >>> data = numpy.zeros(shape=(1,1,1))
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
    >>> starts = pandas.DatetimeIndex([pandas.Timestamp('2012-05-01')])
    >>> ends = pandas.DatetimeIndex([pandas.Timestamp('2012-05-02')])
    >>> A = RasterCollectionTile(id="A", extent=extent,
    ...                         data=data, wavelength=420,
    ...                         start_times=starts, end_times=ends)
    >>> B = RasterCollectionTile(id="B", extent=extent,
    ...                         data=data, wavelength=380,
    ...                         start_times=starts, end_times=ends)
    >>> p1 = Point(0,0)
    >>> p2 = Point(100,100)
    >>> p3 = Point(100,0)
    >>> pseries = [p1, p2, p3]
    >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
    >>> data["a"] = [1,2,3]
    >>> data["b"] = ["a","b","c"]
    >>> C = FeatureCollectionTile(id="C", data=data)
    >>> D = FeatureCollectionTile(id="D", data=data)
    >>> udf_data = UdfData(proj={"EPSG":4326}, raster_collection_tiles=[A, B],
    ...                        feature_collection_tiles=[C, D])
    >>> udf_data.add_model_path("scikit-learn", "random_forest", "/tmp/model.p")
    >>> print(udf_data.get_raster_collection_tile_by_id("A"))
    id: A
    extent: north: 100
    south: 0
    east: 100
    west: 0
    nsres: 10
    ewres: 10
    wavelength: 420
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data: [[[0.]]]
    >>> print(udf_data.get_raster_collection_tile_by_id("B"))
    id: B
    extent: north: 100
    south: 0
    east: 100
    west: 0
    nsres: 10
    ewres: 10
    wavelength: 380
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data: [[[0.]]]
    >>> print(udf_data.get_raster_collection_tile_by_id("C"))
    None
    >>> print(udf_data.get_feature_collection_tile_by_id("C"))
    id: C
    start_times: None
    end_times: None
    data:    a  b         geometry
    0  1  a      POINT (0 0)
    1  2  b  POINT (100 100)
    2  3  c    POINT (100 0)
    >>> print(udf_data.get_feature_collection_tile_by_id("D"))
    id: D
    start_times: None
    end_times: None
    data:    a  b         geometry
    0  1  a      POINT (0 0)
    1  2  b  POINT (100 100)
    2  3  c    POINT (100 0)
    >>> print(len(udf_data.get_feature_collection_tiles()) == 2)
    True
    >>> print(len(udf_data.get_raster_collection_tiles()) == 2)
    True
    >>> print(udf_data.models['scikit-learn']['path'])
    /tmp/model.p
    >>> print(udf_data.models['scikit-learn']['model_id'])
    random_forest

    >>> from flask import json
    >>> json.dumps(udf_data.to_dict()) # doctest: +ELLIPSIS
    ...                                # doctest: +NORMALIZE_WHITESPACE
    '{"feature_collection_tiles": [{"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"},
                                    "id": "0", "properties": {"a": 1, "b": "a"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 100.0], "type": "Point"}, "id": "1",
                                    "properties": {"a": 2, "b": "b"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 0.0], "type": "Point"}, "id": "2",
                                    "properties": {"a": 3, "b": "c"}, "type": "Feature"}],
                                    "type": "FeatureCollection"}, "id": "C"},
                                   {"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"},
                                    "id": "0", "properties": {"a": 1, "b": "a"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 100.0], "type": "Point"}, "id": "1",
                                    "properties": {"a": 2, "b": "b"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 0.0], "type": "Point"}, "id": "2",
                                    "properties": {"a": 3, "b": "c"}, "type": "Feature"}],
                                    "type": "FeatureCollection"}, "id": "D"}],
       "models": {"scikit-learn": {"model_id": "random_forest", "path": "/tmp/model.p"}},
       "proj": {"EPSG": 4326},
       "raster_collection_tiles": [{"data": [[[0.0]]],
                                   "end_times": ["2012-05-02T00:00:00"],
                                   "extent": {"east": 100, "ewres": 10, "north": 100, "nsres": 10, "south": 0, "west": 0},
                                   "id": "A",
                                   "start_times": ["2012-05-01T00:00:00"],
                                   "wavelength": 420},
                                  {"data": [[[0.0]]],
                                   "end_times": ["2012-05-02T00:00:00"],
                                   "extent": {"east": 100, "ewres": 10, "north": 100, "nsres": 10, "south": 0, "west": 0},
                                   "id": "B",
                                   "start_times": ["2012-05-01T00:00:00"],
                                   "wavelength": 380}]}'

    >>> udf = UdfData.from_dict(udf_data.to_dict())
    >>> json.dumps(udf.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"feature_collection_tiles": [{"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"},
                                    "id": "0", "properties": {"a": 1, "b": "a"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 100.0], "type": "Point"}, "id": "1",
                                    "properties": {"a": 2, "b": "b"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 0.0], "type": "Point"}, "id": "2",
                                    "properties": {"a": 3, "b": "c"}, "type": "Feature"}],
                                    "type": "FeatureCollection"}, "id": "C"},
                                   {"data": {"features": [{"geometry": {"coordinates": [0.0, 0.0], "type": "Point"},
                                    "id": "0", "properties": {"a": 1, "b": "a"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 100.0], "type": "Point"}, "id": "1",
                                    "properties": {"a": 2, "b": "b"}, "type": "Feature"},
                                   {"geometry": {"coordinates": [100.0, 0.0], "type": "Point"}, "id": "2",
                                    "properties": {"a": 3, "b": "c"}, "type": "Feature"}],
                                    "type": "FeatureCollection"}, "id": "D"}],
       "models": {"scikit-learn": {"model_id": "random_forest", "path": "/tmp/model.p"}},
       "proj": {"EPSG": 4326},
       "raster_collection_tiles": [{"data": [[[0.0]]],
                                   "end_times": ["2012-05-02T00:00:00"],
                                   "extent": {"east": 100, "ewres": 10, "north": 100, "nsres": 10, "south": 0, "west": 0},
                                   "id": "A",
                                   "start_times": ["2012-05-01T00:00:00"],
                                   "wavelength": 420},
                                  {"data": [[[0.0]]],
                                   "end_times": ["2012-05-02T00:00:00"],
                                   "extent": {"east": 100, "ewres": 10, "north": 100, "nsres": 10, "south": 0, "west": 0},
                                   "id": "B",
                                   "start_times": ["2012-05-01T00:00:00"],
                                   "wavelength": 380}]}'

    """

    def __init__(self, proj, raster_collection_tiles=None, feature_collection_tiles=None):
        """The constructor of the UDF argument class that stores all data required by the
        user defined function.

        Args:
            proj (dict): A dictionary of form {"proj type string": "projection decription"} i. e. {"EPSG":4326}
            raster_collection_tiles (list[RasterCollectionTile]): A list of RasterCollectionTile objects
            feature_collection_tiles (list[FeatureCollectionTile]): A list of VectorTile objects
        """

        self._raster_tile_list = []
        self._feature_tile_list = []
        self._raster_tile_dict = {}
        self._feature_tile_dict = {}
        self.proj = proj
        self.models = {}

        self.set_raster_collection_tiles(raster_collection_tiles=raster_collection_tiles)
        self.set_feature_collection_tiles(feature_collection_tiles=feature_collection_tiles)

    def get_raster_collection_tile_by_id(self, id):
        """Get an raster collection tile by its id

        Args:
            id (str): The raster collection tile id

        Returns:
            RasterCollectionTile: the requested raster collection tile of None if not found

        """
        if id in self._raster_tile_dict:
            return self._raster_tile_dict[id]
        return None

    def get_feature_collection_tile_by_id(self, id):
        """Get a vector tile by its id

        Args:
            id (str): The vector tile id

        Returns:
            FeatureCollectionTile: the requested vector tile of None if not found

        """
        if id in self._feature_tile_dict:
            return self._feature_tile_dict[id]
        return None

    def get_raster_collection_tiles(self):
        """Get all raster collection tiles

        Returns:
            list[RasterCollectionTile]: The list of raster collection tiles

        """
        return self._raster_tile_list

    def set_raster_collection_tiles(self, raster_collection_tiles):
        """Set the raster collection tiles list

        If raster_collection_tiles is None, then the list will be cleared

        Args:
            raster_collection_tiles (list[RasterCollectionTile]): A list of RasterCollectionTile's
        """

        self.get_raster_collection_tiles()
        if raster_collection_tiles is None:
            return

        for entry in raster_collection_tiles:
            self.append_raster_collection_tile(entry)

    def del_raster_collection_tiles(self):
        """Delete all raster collection tiles
        """
        self._raster_tile_list.clear()
        self._raster_tile_dict.clear()

    def get_feature_collection_tiles(self):
        """Get all feature collection tiles

        Returns:
            list[FeatureCollectionTile]: The list of feature collection tiles

        """
        return self._feature_tile_list

    def set_feature_collection_tiles(self, feature_collection_tiles):
        """Set the feature collection tiles

        If feature_collection_tiles is None, then the list will be cleared

        Args:
            feature_collection_tiles (list[FeatureCollectionTile]): A list of FeatureCollectionTile's
        """

        self.del_feature_collection_tiles()
        if feature_collection_tiles is None:
            return

        for entry in feature_collection_tiles:
            self.append_feature_collection_tile(entry)

    def del_feature_collection_tiles(self):
        """Delete all feature collection tiles
        """
        self._feature_tile_list.clear()
        self._feature_tile_dict.clear()

    raster_collection_tiles = property(fget=get_raster_collection_tiles,
                                       fset=set_raster_collection_tiles, fdel=del_raster_collection_tiles)
    feature_collection_tiles = property(fget=get_feature_collection_tiles,
                                        fset=set_feature_collection_tiles, fdel=del_feature_collection_tiles)

    def append_raster_collection_tile(self, image_collection_tile):
        """Append a raster collection tile to the list

        It will be automatically added to the dictionary of all raster collection tiles

        Args:
            image_collection_tile (RasterCollectionTile): The raster collection tile to append
        """
        self._raster_tile_list.append(image_collection_tile)
        self._raster_tile_dict[image_collection_tile.id] = image_collection_tile

    def append_feature_collection_tile(self, feature_collection_tile):
        """Append a feature collection tile to the list

        It will be automatically added to the dictionary of all feature collection tiles

        Args:
            feature_collection_tile (FeatureCollectionTile): The feature collection tile to append
        """
        self._feature_tile_list.append(feature_collection_tile)
        self._feature_tile_dict[feature_collection_tile.id] = feature_collection_tile

    def add_model_path(self, framework, model_id, path):
        """Add a model path to the UDF object

        Args:
            framework (str): The name of the framework (scikit-learn, pytorch, tensorflow)
            model_id (str): The unique od of the model
            path (str): The path to the model

        Returns:

        """
        self.models[framework] = dict(model_id=model_id, path=path)

    def to_dict(self):
        """Convert this UdfData object into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            UdfData object as a dictionary
        """

        d = {"proj": self.proj}

        if self._raster_tile_list is not None:
            l = []
            for tile in self._raster_tile_list:
                l.append(tile.to_dict())
            d["raster_collection_tiles"] = l

        if self._feature_tile_list is not None:
            l = []
            for tile in self._feature_tile_list:
                l.append(tile.to_dict())
            d["feature_collection_tiles"] = l

        if self.models is not None:
            d["models"] = self.models

        return d

    @staticmethod
    def from_dict(udf_dict):
        """Create a udf data object from a python dictionary that was created from
        the JSON definition of the UdfData class

        Args:
            udf_dict (dict): The dictionary that contains the udf data definition

        Returns:
            UdfData:
            A new UdfData object

        """

        if "proj" not in udf_dict:
            raise Exception("Missing projection in dictionary")

        udf_data = UdfData(proj=udf_dict["proj"])

        if "raster_collection_tiles" in udf_dict:
            l = udf_dict["raster_collection_tiles"]
            for entry in l:
                rct = RasterCollectionTile.from_dict(entry)
                udf_data.append_raster_collection_tile(rct)

        if "feature_collection_tiles" in udf_dict:
            l = udf_dict["feature_collection_tiles"]
            for entry in l:
                fct = FeatureCollectionTile.from_dict(entry)
                udf_data.append_feature_collection_tile(fct)

        if "models" in udf_dict:
            udf_data.models = udf_dict["models"]

        return udf_data


if __name__ == "__main__":
    import doctest
    doctest.testmod()
