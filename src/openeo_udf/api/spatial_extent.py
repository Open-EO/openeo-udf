#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes of the OpenEO Python UDF interface

"""
from shapely.geometry import Polygon, Point
from typing import Optional, Dict, Tuple


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

    def __init__(self, top: float, bottom: float, right: float, left: float,
                 height: Optional[float]=None, width: Optional[float]=None):
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

    def contains_point(self, top: float, left: float) -> Point:
        """Return True if the provided coordinate is located in the spatial extent, False otherwise

        Args:
           top (float): The top (northern) coordinate of the point
           left (float): The left (western) coordinate of the point


        Returns:
            bool: True if the coordinates are contained in the extent, False otherwise

        """
        return self.polygon.contains(Point(left, top))
        # return self.polygon.intersects(Point(left, top))

    def to_index(self, top: float, left: float) -> Tuple[int, int]:
        """Return True if the provided coordinate is located in the spatial extent, False otherwise

        Args:
           top (float): The top (northern) coordinate
           left (float): The left (western) coordinate

        Returns:
             tuple(int, int): (x, y) The x, y index

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

    def as_polygon(self) -> Polygon:
        """Return the extent as shapely.geometry.Polygon to perform
        comparison operations between other extents like equal, intersect and so on

        Returns:
            shapely.geometry.Polygon: The polygon representing the spatial extent

        """

        return Polygon([(self.left, self.top),(self.right, self.top),
                        (self.right, self.bottom),(self.left, self.bottom)])

    @staticmethod
    def from_polygon(polygon: Polygon) -> 'SpatialExtent':
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

    def to_dict(self) -> Dict:
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
    def from_dict(extent: Dict):
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
