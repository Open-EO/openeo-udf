#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

import numpy
import xarray
from typing import Dict, List


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class DataCube:
    """This class is a hypercube representation of multi-dimensional data
    that stores an xarray and provides methods to convert the xarray into
    the HyperCube JSON representation


    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)), coords={'x': [1, 2], 'y': [1, 2, 3]}, dims=('x', 'y'))
    >>> array.attrs["description"] = "This is an xarray with two dimensions"
    >>> array.name = "testdata"
    >>> h = DataCube(array=array)
    >>> d = h.to_dict()
    >>> d["id"]
    'testdata'
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> d["description"]
    'This is an xarray with two dimensions'

    >>> new_h = DataCube.from_dict(d)
    >>> d = new_h.to_dict()
    >>> d["id"]
    'testdata'
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> d["description"]
    'This is an xarray with two dimensions'

    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)), coords={'x': [1, 2], 'y': [1, 2, 3]}, dims=('x', 'y'))
    >>> h = DataCube(array=array)
    >>> d = h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> "description" not in d
    True

    >>> new_h = DataCube.from_dict(d)
    >>> d = new_h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> "description" not in d
    True

    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)))
    >>> h = DataCube(array=array)
    >>> d = h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    []
    >>> "description" not in d
    True

    >>> new_h = DataCube.from_dict(d)
    >>> d = new_h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    []
    >>> "description" not in d
    True

    """

    def __init__(self, array: xarray.DataArray):

        self.set_array(array)

    def __str__(self):
        return "id: %(id)s\n" \
               "data: %(data)s"%{"id":self.id, "data":self.array}

    def get_array(self) -> xarray.DataArray:
        """Return the xarray.DataArray that contains the data and dimension definition

        Returns:
            xarray.DataArray: that contains the data and dimension definition

        """
        return self._array

    def set_array(self, array: xarray.DataArray):
        """Set the xarray.DataArray that contains the data and dimension definition

        This function will check if the provided data is a geopandas.GeoDataFrame and raises
        an Exception

        Args:
            array: xarray.DataArray that contains the data and dimension definition

        """
        if isinstance(array, xarray.DataArray) is False:
            raise Exception("Argument data must be of type xarray.DataArray")

        self._array = array

    @property
    def id(self):
        return self._array.name

    array = property(fget=get_array, fset=set_array)

    def to_dict(self) -> Dict:
        """Convert this hypercube into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            HyperCube as a dictionary

        >>> example = {
        ...     "id": "test_data",
        ...     "data": [
        ...         [
        ...             [0.0, 0.1],
        ...             [0.2, 0.3]
        ...         ],
        ...         [
        ...             [0.0, 0.1],
        ...             [0.2, 0.3]
        ...         ]
        ...     ],
        ...     "dimension": [{"name": "time", "unit": "ISO:8601", "coordinates":["2001-01-01", "2001-01-02"]},
        ...                   {"name": "X", "unit": "degree", "coordinates":[50.0, 60.0]},
        ...                   {"name": "Y", "unit": "degree"},
        ...                  ]
        ... }
        
        """

        d = {"id":"", "data": "", "dimensions":[]}
        if self._array is not None:
            xd = self._array.to_dict()

            if "name" in xd:
                d["id"] = xd["name"]

            if "data" in xd:
                d["data"] = xd["data"]

            if "attrs" in xd:
                if "description" in xd["attrs"]:
                    d["description"] = xd["attrs"]["description"]

            if "dims" in xd and "coords" in xd:
                for dim in xd["dims"]:
                    if dim in xd["coords"]:
                        if "data" in xd["coords"][dim]:
                            d["dimensions"].append({"name": dim, "coordinates": xd["coords"][dim]["data"]})
                        else:
                            d["dimensions"].append({"name": dim})

        return d

    @staticmethod
    def from_dict(hc_dict: Dict) -> "DataCube":
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

        coords = {}
        dims = list()

        if "dimensions" in hc_dict:
            for dim in hc_dict["dimensions"]:
                dims.append(dim["name"])
                if "coordinates" in dim:
                    coords[dim["name"]] = dim["coordinates"]

        if dims and coords:
            data = xarray.DataArray(numpy.asarray(hc_dict["data"]), coords=coords, dims=dims)
        elif dims:
            data = xarray.DataArray(numpy.asarray(hc_dict["data"]), dims=dims)
        else:
            data = xarray.DataArray(numpy.asarray(hc_dict["data"]))

        if "id" in hc_dict:
            data.name = hc_dict["id"]
        if "description" in hc_dict:
            data.attrs["description"] = hc_dict["description"]

        hc = DataCube(array=data)

        return hc

    def to_data_collection(self):
        pass

    @staticmethod
    def from_data_collection(data_collection: 'openeo_udf.server.data_model.data_collection_schema.DataCollectionModel') -> List['DataCube']:
        """Create data cubes from a data collection

        Args:
            data_collection:

        Returns:
            A list of data cubes

        """

        dc_list = []

        data_cubes = data_collection.object_collections.data_cubes
        variables_collections = data_collection.variables_collections

        for cube in data_cubes:
            variable_collection = variables_collections[cube.variable_collection]

            # Read the one dimensional array and reshape it
            coords = {}
            for key in cube.dimensions.keys():
                d = cube.dimensions[key]
                if d.values:
                    coords[key] = d.values
                else:
                    l = d.number_of_cells
                    if l != 0 and d.extent:
                        stepsize = (d.extent[1] - d.extent[0])/l
                        values = []
                        predecessor = d.extent[0]
                        for i in range(l):
                            value = predecessor + stepsize/2.0
                            values.append(value)
                            predecessor = predecessor + stepsize
                        coords[key] = values

            for variable in variable_collection.variables:
                array = numpy.asarray(variable.values)
                array = array.reshape(variable_collection.size)

                data = xarray.DataArray(array, dims=cube.dim, coords=coords)
                data.name = variable.name

                dc = DataCube(array=data)
                dc_list.append(dc)

        return dc_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()
