#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes of the OpenEO Python UDF interface

"""
import geopandas
import pandas
import numpy
import xarray
from shapely.geometry import Polygon, Point
import json


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class SpatialExtent(object):
    """The axis aligned spatial extent of a collection tile

    Some basic tests:

    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=10, width=10)
    >>> print(extent)
    top: 100
    bottom: 0
    right: 100
    left: 0
    height: 10
    width: 10
    >>> extent.to_index(50, 50)
    (5, 5)
    >>> extent.to_index(0, 0)
    (0, 10)
    >>> extent.to_index(100, 0)
    (0, 0)

    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0)
    >>> print(extent)
    top: 100
    bottom: 0
    right: 100
    left: 0
    height: None
    width: None
    >>> p = extent.as_polygon()
    >>> print(p)
    POLYGON ((0 100, 100 100, 100 0, 0 0, 0 100))

    >>> from shapely.wkt import loads
    >>> p = loads("POLYGON ((0 100, 100 100, 100 0, 0 0, 0 100))")
    >>> extent = SpatialExtent.from_polygon(p)
    >>> print(extent)
    top: 100.0
    bottom: 0.0
    right: 100.0
    left: 0.0
    height: None
    width: None
    >>> extent.contains_point(50, 50)
    True
    >>> extent.contains_point(150, 50)
    False
    >>> extent.contains_point(25, 25)
    True
    >>> extent.contains_point(101, 101)
    False

    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0)
    >>> extent.as_polygon() == extent.as_polygon()
    True
    >>> diff = extent.as_polygon() - extent.as_polygon()
    >>> print(diff)
    GEOMETRYCOLLECTION EMPTY

    >>> extent_1 = SpatialExtent(top=80, bottom=10, right=80, left=10)
    >>> extent_2 = SpatialExtent(top=100, bottom=0, right=100, left=0)
    >>> extent_1.as_polygon() == extent_2.as_polygon()
    False
    >>> extent_2.as_polygon().contains(extent_2.as_polygon())
    True

    """

    def __init__(self, top, bottom, right, left, height=None, width=None):
        """Constructor of the axis aligned spatial extent of a collection tile

        Args:
            top (float): The top (northern) border of the data chunk
            bottom (float): The bottom (southern) border of the data chunk
            right (float): The righ (eastern) border of the data chunk
            left (float): The left (western) border of the data chunk
            height (float): The top-bottom pixel resolution (ignored in case of vector data chunks)
            width (float): The right-left pixel resolution (ignored in case of vector data chunks)

        """

        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left
        self.height = height
        self.width = width
        self.polygon = self.as_polygon()

    def contains_point(self, top, left):
        """Return True if the provided coordinate is located in the spatial extent, False otherwise

        Args:
           top (float): The top (northern) coordinate of the point
           left (float): The left (western) coordinate of the point


        Returns:
            bool: True if the coordinates are contained in the extent, False otherwise

        """
        return self.polygon.contains(Point(left, top))
        # return self.polygon.intersects(Point(left, top))

    def to_index(self, top, left):
        """Return True if the provided coordinate is located in the spatial extent, False otherwise

        Args:
           top (float): The top (northern) coordinate
           left (float): The left (western) coordinate

        Returns:
             tuple(int): (x, y) The x, y index

        """
        x = int(abs((left - self.left)/self.width))
        y = int(abs((top - self.top)/self.height))
        return (x, y)

    def __str__(self):
        return "top: %(n)s\n" \
               "bottom: %(s)s\n" \
               "right: %(e)s\n" \
               "left: %(w)s\n" \
               "height: %(ns)s\n" \
               "width: %(ew)s"%{"n":self.top, "s":self.bottom, "e":self.right,
                                "w":self.left, "ns":self.height, "ew":self.width}

    def as_polygon(self):
        """Return the extent as shapely.geometry.Polygon to perform
        comparison operations between other extents like equal, intersect and so on

        Returns:
            shapely.geometry.Polygon: The polygon representing the spatial extent

        """

        return Polygon([(self.left, self.top),(self.right, self.top),
                        (self.right, self.bottom),(self.left, self.bottom)])

    @staticmethod
    def from_polygon(polygon):
        """Convert a polygon with rectangular shape into a spatial extent

        Args:
            polygon (shapely.geometry.Polygon): The polygon that should be converted into a spatial extent

        Returns:
            SpatialExtent: The spatial extent

        """

        coords = list(polygon.exterior.coords)

        top = coords[0][1]
        bottom = coords[2][1]
        right = coords[1][0]
        left = coords[0][0]

        return SpatialExtent(top=top, bottom=bottom, right=right, left=left)

    def to_dict(self):
        """Return the spatial extent as a dict that can be easily converted into JSON

        Returns:
            dict:
            Dictionary representation

        """
        d = dict(extent=dict(top=self.top, bottom=self.bottom, right=self.right,
                             left=self.left))

        if self.width:
            d["extent"].update({"width":self.width})
        if self.height:
            d["extent"].update({"height":self.height})

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

        top = None
        bottom = None
        right = None
        left = None
        width = None
        height = None

        if "top" in extent:
            top = extent["top"]
        if "bottom" in extent:
            bottom = extent["bottom"]
        if "right" in extent:
            right = extent["right"]
        if "left" in extent:
            left = extent["left"]
        if "width" in extent:
            width = extent["width"]
        if "height" in extent:
            height = extent["height"]

        return SpatialExtent(top=top, bottom=bottom, left=left, right=right, height=height, width=width)


class CollectionTile(object):
    """This is the base class for image and vector collection tiles. It implements
    start time, end time and spatial extent handling.

    Some basic tests:

    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=10, width=10)
    >>> coll = CollectionTile(id="test", extent=extent)
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
    >>> rdc = CollectionTile(id="test", extent=extent,
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

    >>> ct = CollectionTile(id="test")
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

    def sample(self, top, left):
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


class HyperCube:
    """This class is a hypercube representation of multi-dimensional data


    >>> data = xarray.DataArray(numpy.random.randn(2, 3))
    >>> data.to_dict()

    """

    def __init__(self, id: str, data: xarray.DataArray):

        self.id = id
        self.set_data(data)

    def __str__(self):
        return "id: %(id)s\n" \
               "data: %(data)s"%{"id":self.id, "data":self.data}

    def get_data(self) -> xarray.DataArray:
        """Return the xarray.DataArray that contains the data and dimension definition

        Returns:
            xarray.DataArray: that contains the data and dimension definition

        """
        return self._data

    def set_data(self, data: xarray.DataArray):
        """Set the xarray.DataArray that contains the data and dimension definition

        This function will check if the provided data is a geopandas.GeoDataFrame and raises
        an Exception

        Args:
            data: xarray.DataArray that contains the data and dimension definition

        """
        if isinstance(data, xarray.DataArray) is False:
            raise Exception("Argument data must be of type xarray.DataArray")

        self._data = data

    data = property(fget=get_data, fset=set_data)

    def to_dict(self) -> dict:
        """Convert this hypercube into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            HyperCube as a dictionary
        """

        d = {"id": self.id}
        if self._data is not None:
            d["data"] = self._data.to_dict()

        return d

    @staticmethod
    def from_dict(hc_dict: dict) -> "HyperCube":
        """Create a hypercube from a python dictionary that was created from
        the JSON definition of the HyperCube

        Args:
            hc_dict (dict): The dictionary that contains the hypercube definition

        Returns:
            HyperCube

        """

        if "id" not in hc_dict:
            raise Exception("Missing id in dictionary")

        if "data" not in hc_dict:
            raise Exception("Missing data in dictionary")

        hc = HyperCube(id=hc_dict["id"],
                       data=xarray.DataArray(numpy.asarray(hc_dict["data"])))

        return hc

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
    >>> fct = FeatureCollectionTile(id="test", start_times=starts, end_times=ends, data=data)
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

    >>> fct = FeatureCollectionTile.from_dict(fct.to_dict())
    >>> json.dumps(fct.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"id": "test", "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"],
    "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature",
    "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}]}}'

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


class StructuredData(object):
    """This class represents structured data that is produced by an UDF and can not be represented
    as a RasterCollectionTile or FeatureCollectionTile. For example the result of a statistical
    computation. The data is self descriptive and supports the basic types dict/map, list and table.

    The data field contains the UDF specific values (argument or return) as dict, list or table:

        * A dict can be as complex as required by the UDF
        * A list must contain simple data types example {\"list\": [1,2,3,4]}
        * A table is a list of lists with a header, example {\"table\": [[\"id\",\"value\"],
                                                                           [1,     10],
                                                                           [2,     23],
                                                                           [3,     4]]}

    """

    def __init__(self, description, data, type):
        self.description = description
        self.data = data
        self.type = type

    def to_dict(self):
        return dict(description=self.description, data=self.data, type=self.type)

    @staticmethod
    def from_dict(structured_data):
        description = structured_data["description"]
        data = structured_data["data"]
        type = structured_data["type"]
        return StructuredData(description=description, data=data, type=type)


class MachineLearnModel(object):
    """This class represents a machine learn model. The model will be loaded
    at construction, based on the machine learn framework.

    The following frameworks are supported:
        - sklearn models that are created with sklearn.externals.joblib
        - pytorch models that are created with torch.save

    >>> from sklearn.ensemble import RandomForestRegressor
    >>> from sklearn.externals import joblib
    >>> model = RandomForestRegressor(n_estimators=10, max_depth=2, verbose=0)
    >>> path = '/tmp/test.pkl.xz'
    >>> dummy = joblib.dump(value=model, filename=path, compress=("xz", 3))
    >>> m = MachineLearnModel(framework="sklearn", name="test",
    ...                       description="Machine learn model", path=path)
    >>> m.get_model()# doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
               max_features='auto', max_leaf_nodes=None,
               min_impurity_decrease=0.0, min_impurity_split=None,
               min_samples_leaf=1, min_samples_split=2,
               min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
               oob_score=False, random_state=None, verbose=0, warm_start=False)
    >>> m.to_dict() # doctest: +ELLIPSIS
    ...             # doctest: +NORMALIZE_WHITESPACE
    {'description': 'Machine learn model', 'name': 'test', 'framework': 'sklearn', 'path': '/tmp/test.pkl.xz'}
    >>> d = {'description': 'Machine learn model', 'name': 'test', 'framework': 'sklearn', 'path': '/tmp/test.pkl.xz'}
    >>> m = MachineLearnModel.from_dict(d)
    >>> m.get_model() # doctest: +ELLIPSIS
    ...               # doctest: +NORMALIZE_WHITESPACE
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
               max_features='auto', max_leaf_nodes=None,
               min_impurity_decrease=0.0, min_impurity_split=None,
               min_samples_leaf=1, min_samples_split=2,
               min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
               oob_score=False, random_state=None, verbose=0, warm_start=False)

    >>> import torch
    >>> import torch.nn as nn
    >>> model = nn.Module
    >>> path = '/tmp/test.pt'
    >>> torch.save(model, path)
    >>> m = MachineLearnModel(framework="pytorch", name="test",
    ...                       description="Machine learn model", path=path)
    >>> m.get_model()# doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    <class 'torch.nn.modules.module.Module'>
    >>> m.to_dict() # doctest: +ELLIPSIS
    ...             # doctest: +NORMALIZE_WHITESPACE
    {'description': 'Machine learn model', 'name': 'test', 'framework': 'pytorch', 'path': '/tmp/test.pt'}
    >>> d = {'description': 'Machine learn model', 'name': 'test', 'framework': 'pytorch', 'path': '/tmp/test.pt'}
    >>> m = MachineLearnModel.from_dict(d)
    >>> m.get_model() # doctest: +ELLIPSIS
    ...               # doctest: +NORMALIZE_WHITESPACE
    <class 'torch.nn.modules.module.Module'>
    """

    def __init__(self, framework, name, description, path):
        self.framework = framework
        self.name = name
        self.description = description
        self.path = path
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the machine learn model from the path.

        Supported model:
        - sklearn models that are created with sklearn.externals.joblib
        - pytorch models that are created with torch.save

        """
        if self.framework.lower() in "sklearn":
            from sklearn.externals import joblib
            self.model = joblib.load(self.path)
        if self.framework.lower() in "pytorch":
            import torch
            self.model = torch.load(self.path)

    def get_model(self):
        """Get the loaded machine learn model. This function will return None if the model was not loaded

        :return: the loaded model
        """
        return self.model

    def to_dict(self):
        return dict(description=self.description, name=self.name, framework=self.framework, path=self.path)

    @staticmethod
    def from_dict(machine_learn_model):
        description = machine_learn_model["description"]
        name = machine_learn_model["name"]
        framework = machine_learn_model["framework"]
        path = machine_learn_model["path"]
        return MachineLearnModel(description=description, name=name, framework=framework, path=path)


class UdfData(object):
    """The class that stores the arguments for a user defined function (UDF)

    Some basic tests:

    >>> from shapely.geometry import Point
    >>> import geopandas
    >>> import numpy, pandas
    >>> from sklearn.ensemble import RandomForestRegressor
    >>> from sklearn.externals import joblib
    >>> data = numpy.zeros(shape=(1,1,1))
    >>> extent = SpatialExtent(top=100, bottom=0, right=100, left=0, height=10, width=10)
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
    >>> model = RandomForestRegressor(n_estimators=10, max_depth=2, verbose=0)
    >>> path = '/tmp/test.pkl.xz'
    >>> dummy = joblib.dump(value=model, filename=path, compress=("xz", 3))
    >>> m = MachineLearnModel(framework="sklearn", name="test",
    ...                       description="Machine learn model", path=path)
    >>> udf_data.append_machine_learn_model(m)
    >>> print(udf_data.get_raster_collection_tile_by_id("A"))
    id: A
    extent: top: 100
    bottom: 0
    right: 100
    left: 0
    height: 10
    width: 10
    wavelength: 420
    start_times: DatetimeIndex(['2012-05-01'], dtype='datetime64[ns]', freq=None)
    end_times: DatetimeIndex(['2012-05-02'], dtype='datetime64[ns]', freq=None)
    data: [[[0.]]]
    >>> print(udf_data.get_raster_collection_tile_by_id("B"))
    id: B
    extent: top: 100
    bottom: 0
    right: 100
    left: 0
    height: 10
    width: 10
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
    >>> print(udf_data.ml_model_list[0].path)
    /tmp/test.pkl.xz
    >>> print(udf_data.ml_model_list[0].framework)
    sklearn

    >>> import json
    >>> json.dumps(udf_data.to_dict()) # doctest: +ELLIPSIS
    ...                                # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "raster_collection_tiles": [{"id": "A", "data": [[[0.0]]], "wavelength": 420, "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"], "extent": {"top": 100, "bottom": 0, "right": 100, "left": 0, "width": 10, "height": 10}}, {"id": "B", "data": [[[0.0]]], "wavelength": 380, "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"], "extent": {"top": 100, "bottom": 0, "right": 100, "left": 0, "width": 10, "height": 10}}], "feature_collection_tiles": [{"id": "C", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}, {"id": "D", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}], "structured_data_list": [], "machine_learn_models": [{"description": "Machine learn model", "name": "test", "framework": "sklearn", "path": "/tmp/test.pkl.xz"}]}'

    >>> udf = UdfData.from_dict(udf_data.to_dict())
    >>> json.dumps(udf.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "raster_collection_tiles": [{"id": "A", "data": [[[0.0]]], "wavelength": 420, "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"], "extent": {"top": 100, "bottom": 0, "right": 100, "left": 0, "width": 10, "height": 10}}, {"id": "B", "data": [[[0.0]]], "wavelength": 380, "start_times": ["2012-05-01T00:00:00"], "end_times": ["2012-05-02T00:00:00"], "extent": {"top": 100, "bottom": 0, "right": 100, "left": 0, "width": 10, "height": 10}}], "feature_collection_tiles": [{"id": "C", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}, {"id": "D", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}], "structured_data_list": [], "machine_learn_models": [{"description": "Machine learn model", "name": "test", "framework": "sklearn", "path": "/tmp/test.pkl.xz"}]}'

    >>> sd_list = StructuredData(description="Data list", data={"list":[1,2,3]}, type="list")
    >>> sd_dict = StructuredData(description="Data dict", data={"A":{"B": 1}}, type="dict")
    >>> udf = UdfData(proj={"EPSG":4326}, structured_data_list=[sd_list, sd_dict])
    >>> json.dumps(udf.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "raster_collection_tiles": [], "feature_collection_tiles": [], "structured_data_list": [{"description": "Data list", "data": {"list": [1, 2, 3]}, "type": "list"}, {"description": "Data dict", "data": {"A": {"B": 1}}, "type": "dict"}], "machine_learn_models": []}'

    """

    def __init__(self, proj, raster_collection_tiles=None, feature_collection_tiles=None,
                 structured_data_list=None, ml_model_list=None):
        """The constructor of the UDF argument class that stores all data required by the
        user defined function.

        Args:
            proj (dict): A dictionary of form {"proj type string": "projection decription"} i. e. {"EPSG":4326}
            raster_collection_tiles (list[RasterCollectionTile]): A list of RasterCollectionTile objects
            feature_collection_tiles (list[FeatureCollectionTile]): A list of VectorTile objects
            structured_data_list (list[StructuredData]): A list of structured data objects
            ml_model_list (list[MachineLearnModel]): A list of machine learn models
        """

        self._raster_tile_list = []
        self._feature_tile_list = []
        self._raster_tile_dict = {}
        self._feature_tile_dict = {}
        self._structured_data_list = []
        self._ml_model_list = []
        self.proj = proj

        if raster_collection_tiles:
            self.set_raster_collection_tiles(raster_collection_tiles=raster_collection_tiles)
        if feature_collection_tiles:
            self.set_feature_collection_tiles(feature_collection_tiles=feature_collection_tiles)
        if structured_data_list:
            self.set_structured_data_list(structured_data_list=structured_data_list)
        if ml_model_list:
            self.set_ml_model_list(ml_model_list=ml_model_list)

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

        self.del_raster_collection_tiles()
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

    def get_structured_data_list(self):
        """Get all structured data entries

        Returns:
            (list[StructuredData]): A list of StructuredData objects

        """
        return self._structured_data_list

    def set_structured_data_list(self, structured_data_list):
        """Set the list of structured data

        If structured_data_list is None, then the list will be cleared

        Args:
            structured_data_list (list[StructuredData]): A list of StructuredData objects
        """

        self.del_structured_data_list()
        if structured_data_list is None:
            return

        for entry in structured_data_list:
            self._structured_data_list.append(entry)

    def del_structured_data_list(self):
        """Delete all structured data entries
        """
        self._structured_data_list.clear()

    def get_ml_model_list(self):
        """Get all machine learn models

        Returns:
            (list[MachineLearnModel]): A list of MachineLearnModel objects

        """
        return self._ml_model_list

    def set_ml_model_list(self, ml_model_list):
        """Set the list of machine learn models

        If ml_model_list is None, then the list will be cleared

        Args:
            ml_model_list (list[MachineLearnModel]): A list of MachineLearnModel objects
        """

        self.del_ml_model_list()
        if ml_model_list is None:
            return

        for entry in ml_model_list:
            self._ml_model_list.append(entry)

    def del_ml_model_list(self):
        """Delete all machine learn models
        """
        self._ml_model_list.clear()

    raster_collection_tiles = property(fget=get_raster_collection_tiles,
                                       fset=set_raster_collection_tiles, fdel=del_raster_collection_tiles)
    feature_collection_tiles = property(fget=get_feature_collection_tiles,
                                        fset=set_feature_collection_tiles, fdel=del_feature_collection_tiles)
    structured_data_list = property(fget=get_structured_data_list,
                                    fset=set_structured_data_list, fdel=del_structured_data_list)
    ml_model_list = property(fget=get_ml_model_list,
                                  fset=set_ml_model_list, fdel=del_ml_model_list)

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

    def append_structured_data(self, structured_data):
        """Append a structured data object to the list

        Args:
            structured_data (StructuredData): A StructuredData objects
        """
        self._structured_data_list.append(structured_data)

    def append_machine_learn_model(self, machine_learn_model):
        """Append a machine learn model to the list

        Args:
            machine_learn_model (MachineLearnModel): A MachineLearnModel objects
        """
        self._ml_model_list.append(machine_learn_model)

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

        if self._structured_data_list is not None:
            l = []
            for entry in self._structured_data_list:
                l.append(entry.to_dict())
            d["structured_data_list"] = l

        if self._structured_data_list is not None:
            l = []
            for entry in self._structured_data_list:
                l.append(entry.to_dict())
            d["structured_data_list"] = l

        if self._ml_model_list is not None:
            l = []
            for entry in self._ml_model_list:
                l.append(entry.to_dict())
            d["machine_learn_models"] = l

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

        if "structured_data_list" in udf_dict:
            l = udf_dict["structured_data_list"]
            for entry in l:
                sd = StructuredData.from_dict(entry)
                udf_data.append_structured_data(sd)

        if "machine_learn_models" in udf_dict:
            l = udf_dict["machine_learn_models"]
            for entry in l:
                mlm = MachineLearnModel.from_dict(entry)
                udf_data.append_machine_learn_model(mlm)

        return udf_data


if __name__ == "__main__":
    import doctest
    doctest.testmod()
