#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes of the OpenEO Python UDF interface

"""
import geopandas
import pandas
import numpy
from shapely.geometry import Polygon

__license__ = "Apache License, Version 2.0"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
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

    """

    def __init__(self, id, extent, start_times=None, end_times=None):
        """Constructor of the base class for tile of a collection

        Args:
            id: The unique id of the image collection tile
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

    Some basic tests:

    >>> import numpy, pandas
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

    def __init__(self, id, extent, data, wavelength=None, start_times=None, end_times=None):
        """Constructor of the tile of an image collection

        Args:
            id (str): The unique id of the image collection tile
            extent (SpatialExtent): The spatial extent with resolution information
            data (numpy.ndarray): The three dimensional numpy.ndarray with indices [t][y][x]
            wavelength (float): The optional wavelength of the data chunk
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


class VectorTile(CollectionTile):
    """A vector collection tile that represents a subset or a whole vector dataset
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
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0)
    >>> vdc = VectorTile(id="test", extent=extent, data=data)
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

    def __init__(self, id, extent, data, start_times=None, end_times=None):
        """Constructor of the tile of a vector collection

        Args:
            id (str): The unique id of the vector collection tile
            extent (SpatialExtent): The spatial extent with resolution information
            data (geopandas.GeoDataFrame): A GeoDataFrame with geometry column and attribute data
            start_times (pandas.DateTimeIndex): The vector with start times for each spatial x,y slice
            end_times (pandas.DateTimeIndex): The pandas.DateTimeIndex vector with end times for each spatial x,y slice, if no
                       end times are defined, then time instances are assumed not intervals
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


class UdfArgument(object):
    """The class that stores the arguments for a user defined function (UDF)

    Some basic tests:

    >>> from shapely.geometry import Point
    >>> import geopandas
    >>> import numpy, pandas
    >>> data = numpy.zeros(shape=(1,1,1))
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0, nsres=10, ewres=10)
    >>> starts = pandas.DatetimeIndex([pandas.Timestamp('2012-05-01')])
    >>> ends = pandas.DatetimeIndex([pandas.Timestamp('2012-05-02')])
    >>> A = ImageCollectionTile(id="A", extent=extent,
    ...                         data=data, wavelength=420,
    ...                         start_times=starts, end_times=ends)
    >>> B = ImageCollectionTile(id="B", extent=extent,
    ...                         data=data, wavelength=380,
    ...                         start_times=starts, end_times=ends)
    >>> p1 = Point(0,0)
    >>> p2 = Point(100,100)
    >>> p3 = Point(100,0)
    >>> pseries = [p1, p2, p3]
    >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
    >>> data["a"] = [1,2,3]
    >>> data["b"] = ["a","b","c"]
    >>> extent = SpatialExtent(north=100, south=0, east=100, west=0)
    >>> C = VectorTile(id="C", extent=extent, data=data)
    >>> D = VectorTile(id="D", extent=extent, data=data)
    >>> udf_args = UdfArgument(proj={"EPSG":4326}, image_collection_tiles=[A, B],
    ...                        vector_tiles=[C, D])
    >>> udf_args.add_model_path("scikit-learn", "random_forest", "/tmp/model.p")
    >>> print(udf_args.get_image_collection_tile_by_id("A"))
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
    >>> print(udf_args.get_image_collection_tile_by_id("B"))
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
    >>> print(udf_args.get_image_collection_tile_by_id("C"))
    None
    >>> print(udf_args.get_vector_tile_by_id("C"))
    id: C
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
    >>> print(udf_args.get_vector_tile_by_id("D"))
    id: D
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
    >>> print(len(udf_args.get_vector_tiles()) == 2)
    True
    >>> print(len(udf_args.get_image_collection_tiles()) == 2)
    True
    >>> print(udf_args.models['scikit-learn']['path'])
    /tmp/model.p
    >>> print(udf_args.models['scikit-learn']['model_id'])
    random_forest

    """

    def __init__(self, proj, image_collection_tiles=None, vector_tiles=None):
        """The constructor of the UDF argument class that stores all data required by the
        user defined function.

        Args:
            proj (dict): A dictionary of form {"proj type string": "projection decription"} i. e. {"EPSG":4326}
            image_collection_tiles (list[ImageCollectionTile]): A list of ImageCollectionTile objects
            vector_tiles (list[VectorTile]): A list of VectorTile objects
        """

        self._image_tile_list = []
        self._vector_tile_list = []
        self._image_tile_dict = {}
        self._vector_tile_dict = {}
        self.proj = proj
        self.models = {}

        self.set_image_collection_tiles(image_collection_tiles=image_collection_tiles)
        self.set_vector_tiles(vector_tiles=vector_tiles)

    def get_image_collection_tile_by_id(self, id):
        """Get an image collection tile by its id

        Args:
            id (str): The image collection tile id

        Returns:
            ImageCollectionTile: the requested image collection tile of None if not found

        """
        if id in self._image_tile_dict:
            return self._image_tile_dict[id]
        return None

    def get_vector_tile_by_id(self, id):
        """Get a vector tile by its id

        Args:
            id (str): The vector tile id

        Returns:
            VectorTile: the requested vector tile of None if not found

        """
        if id in self._vector_tile_dict:
            return self._vector_tile_dict[id]
        return None

    def get_image_collection_tiles(self):
        """Get all image collection tiles

        Returns:
            list[ImageCollectionTile]: The list of image collection tiles

        """
        return self._image_tile_list

    def set_image_collection_tiles(self, image_collection_tiles):
        for entry in image_collection_tiles:
            self.append_itc(entry)

    def get_vector_tiles(self):
        return self._vector_tile_list

    def set_vector_tiles(self, vector_tiles):

        for entry in vector_tiles:
            self.append_vtc(entry)

    image_collection_tiles = property(fget=get_image_collection_tiles, fset=set_image_collection_tiles)
    vector_tiles = property(fget=get_vector_tiles, fset=set_vector_tiles)

    def append_itc(self, image_collection_tile):
        self._image_tile_list.append(image_collection_tile)
        self._image_tile_dict[image_collection_tile.id] = image_collection_tile

    def append_vtc(self, vector_collection_tile):
        self._vector_tile_list.append(vector_collection_tile)
        self._vector_tile_dict[vector_collection_tile.id] = vector_collection_tile

    def add_model_path(self, framework, model_id, path):
        """Add a model path to the UDF object

        Args:
            framework (str): The name of the framework (scikit-learn, pytorch, tensorflow)
            model_id (str): The unique od of the model
            path (str): The path to the model

        Returns:

        """
        self.models[framework] = dict(model_id=model_id, path=path)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
