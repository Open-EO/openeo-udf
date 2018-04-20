#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes of the OpenEO Python UDF interface

"""
import geopandas
import pandas
import numpy
from shapely.geometry import Polygon


class SpatialExtent(object):

    def __init__(self, north, south, east, west, nsres=None, ewres=None):
        """Constructor of the axis aligned spatial extent of a data chunk

        Args:
            north: The northern border of the data chunk
            south: The southern border of the data chunk
            east: The eastern border of the data chunk
            west: The west border of the data chunk
            nsres: The north-south pixel resolution (ignored in case of vector data chunks)
            ewres: The east-west pixel resolution (ignored in case of vector data chunks)


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

        """

        return Polygon([(self.west, self.north),(self.east, self.north),
                        (self.east, self.south),(self.west, self.south)])

    @staticmethod
    def from_polygon(polygon):
        """Convert a polygon with rectangular shape into a extent

        Args:
            polygon:

        Returns:

        """

        coords = list(polygon.exterior.coords)

        north = coords[0][1]
        south = coords[2][1]
        east = coords[1][0]
        west = coords[0][0]

        return SpatialExtent(north=north, south=south, east=east, west=west)


class CollectionTile(object):
    """This is the base class for image and vector collection tiles. It implements
    start time, end time and spatial extent handling.

    """

    def __init__(self, id, extent, start_times=None, end_times=None):
        """Constructor of the base class for tile of a collection

        Args:
            id: The unique id of the image collection tile
            extent: The spatial extent with resolution information, must be of type SpatialExtent
            start_times: The pandas.DateTimeIndex vector with start times for each spatial x,y slice
            end_times: The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals


            Some basic tests

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
        return self._start_times

    def set_start_times(self, start_times=None):
        """Set the start times vector that must be of type pandas.DateTimeIndex

        Args:
            start_times:

        """
        if start_times is None:
            return

        if isinstance(start_times, pandas.DatetimeIndex) is False:
            raise Exception("The start times vector mus be of type pandas.DatetimeIndex")

        self._start_times = start_times

    def get_end_times(self):
        return self._end_times

    def set_end_times(self, end_times=None):
        """Set the end times vector that must be of type pandas.DateTimeIndex

        Args:
            end_times:

        Returns:

        """
        if end_times is None:
            return

        if isinstance(end_times, pandas.DatetimeIndex) is False:
            raise Exception("The start times vector mus be of type pandas.DatetimeIndex")

        self._end_times = end_times

    def get_extent(self):
        return self._extent

    def set_extent(self, extent):
        """Set the spatial extent

        Args:
            extent: The spatial extent with resolution information, must be of type SpatialExtent
        """

        if isinstance(extent, SpatialExtent) is False:
            raise Exception("extent mus be of type SpatialExtent")

        self._extent = extent

    start_times = property(fget=get_start_times, fset=set_start_times)
    end_times = property(fget=get_end_times, fset=set_end_times)
    extent = property(fget=get_extent, fset=set_extent)


class ImageCollectionTile(CollectionTile):
    """This class represents a three dimensional image collection tile with
    time information and x,y slices with a single scalar value for each pixel.
    A tile represents a scalar field in space and time,
    for example a time series of a single Landsat 8 or Sentinel2A band. A tile may be a
    spatio-temporal subset of a scalar time series or a whole time series.
    """

    def __init__(self, id, extent, data, wavelength=None, start_times=None, end_times=None):
        """Constructor of the tile of an image collection

        Args:
            id: The unique id of the image collection tile
            extent: The spatial extent with resolution information, must be of type SpatialExtent
            data: The three dimensional numpy.ndarray with indices [t][y][x]
            wavelength: The optional wavelength of the data chunk
            start_times: The pandas.DateTimeIndex vector with start times for each spatial x,y slice
            end_times: The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals


            Some basic tests

            >>> data = numpy.zeros(shape=(1,1,1))
            >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
            >>> rdc = ImageCollectionTile(id="test", extent=extent, data=data, wavelength=420)
            >>> print(rdc)
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
            >>> rdc = ImageCollectionTile(id="test", extent=extent,
            ...                           data=data, wavelength=420,
            ...                           start_times=starts, end_times=ends)
            >>> print(rdc)
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
        return self._data

    def set_data(self, data):
        """Set the three dimensional numpy.ndarray

        This function will check if the provided data is a numpy.ndarray with three dimensions

        Args:
            data:

        """
        if isinstance(data, numpy.ndarray) is False:
            raise Exception("Argument data must be of type numpy.ndarray")

        if len(data.shape) != 3:
            raise Exception("Argument data must have three dimensions")

        self._data = data

    data = property(fget=get_data, fset=set_data)


class VectorCollectionTile(CollectionTile):

    def __init__(self, id, extent, data, start_times=None, end_times=None):
        """Constructor of the tile of a vector collection

        Args:
            id: The unique id of the image collection tile
            extent: The spatial extent with resolution information, must be of type SpatialExtent
            data: A GeoDataFrame with geometry column and attribute data
            start_times: The pandas.DateTimeIndex vector with start times for each spatial x,y slice
            end_times: The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals


            Some basic tests

            >>> from shapely.geometry import Point
            >>> p1 = Point(0,0)
            >>> p2 = Point(100,100)
            >>> p3 = Point(100,0)
            >>> pseries = [p1, p2, p3]
            >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
            >>> data["a"] = [1,2,3]
            >>> data["b"] = ["a","b","c"]
            >>> extent = SpatialExtent(north=100, south=0, east=100, west=0)
            >>> vdc = VectorCollectionTile(id="test", extent=extent, data=data)
            >>> print(vdc)
            id: test
            extent: north: 100
            south: 0
            east: 100
            west: 0
            nsres: None
            ewres: None
            start_times: None
            end_times: None
            data:    a  b         geometry
            0  1  a      POINT (0 0)
            1  2  b  POINT (100 100)
            2  3  c    POINT (100 0)

        """
        CollectionTile.__init__(self, id=id, extent=extent, start_times=start_times, end_times=end_times)

        self.set_data(data)
        self.check_data_with_time()

    def __str__(self):
        return "id: %(id)s\n" \
               "extent: %(extent)s\n" \
               "start_times: %(start_times)s\n" \
               "end_times: %(end_times)s\n" \
               "data: %(data)s"%{"id":self.id, "extent":self.extent,
                                 "start_times":self.start_times,
                                 "end_times":self.end_times, "data":self.data}

    def get_data(self):
        return self._data

    def set_data(self, data):
        """Set the geopandas.GeoDataFrame that contains the geometry column and any number of attribute columns

        This function will check if the provided data is a geopandas.GeoDataFrame and raises

        an Exception

        Args:
            data: geopandas.GeoDataFrame

        """
        if isinstance(data, geopandas.GeoDataFrame) is False:
            raise Exception("Argument data must be of type geopandas.GeoDataFrame")

        self._data = data

    data = property(fget=get_data, fset=set_data)


class UdfArgument(object):

    def __init__(self, proj, image_collection_tiles=None, vector_collection_tiles=None):

        self._image_tile_list = []
        self._vector_tile_list = []
        self._image_tile_dict = {}
        self._vector_tile_dict = {}
        self.proj = proj
        self._models = {"scikit":{}, "pytorch":{}, "tensorflow":{}}

    def get_itc_by_id(self, id):

        if id in self._image_tile_dict:
            return self._image_tile_dict[id]

        return None

    def get_vtc_by_id(self, id):

        if id in self._vector_tile_dict:
            return self._vector_tile_dict[id]

        return None

    def get_image_collection_tiles(self):
        return self._image_tile_list

    def set_image_collection_tiles(self, image_collection_tiles):

        for entry in image_collection_tiles:
            self._image_tile_list.append(entry)
            self._image_tile_dict[entry.id] = entry

    def get_vector_collection_tiles(self):
        return self._vector_tile_list

    def set_vector_collection_tiles(self, vector_collection_tiles):

        for entry in vector_collection_tiles:
            self._vector_tile_list.append(entry)
            self._vector_tile_dict[entry.id] = entry

    icts = property(fget=get_image_collection_tiles, fset=set_image_collection_tiles)
    vcts = property(fget=get_image_collection_tiles, fset=set_image_collection_tiles)

    def append_itc(self, image_collection_tile):
        self._image_tile_list.append(image_collection_tile)
        self._image_tile_dict[image_collection_tile.id] = image_collection_tile

    def append_vtc(self, vector_collection_tile):
        self._vector_tile_list.append(vector_collection_tile)
        self._vector_tile_dict[vector_collection_tile.id] = vector_collection_tile

###############################################################################

if __name__ == "__main__":
    import doctest
    doctest.testmod()
