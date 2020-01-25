#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

import xarray
from typing import Optional, List, Dict
from openeo_udf.api.feature_collection import FeatureCollection
from openeo_udf.api.datacube import DataCube
from openeo_udf.api.machine_learn_model import MachineLearnModel
from openeo_udf.api.spatial_extent import SpatialExtent
from openeo_udf.api.structured_data import StructuredData

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class UdfData:
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
    >>> p1 = Point(0,0)
    >>> p2 = Point(100,100)
    >>> p3 = Point(100,0)
    >>> pseries = [p1, p2, p3]
    >>> data = geopandas.GeoDataFrame(geometry=pseries, columns=["a", "b"])
    >>> data["a"] = [1,2,3]
    >>> data["b"] = ["a","b","c"]
    >>> C = FeatureCollection(id="C", data=data)
    >>> D = FeatureCollection(id="D", data=data)
    >>> udf_data = UdfData(proj={"EPSG":4326}, feature_collection_list=[C, D])
    >>> model = RandomForestRegressor(n_estimators=10, max_depth=2, verbose=0)
    >>> path = '/tmp/test.pkl.xz'
    >>> dummy = joblib.dump(value=model, filename=path, compress=("xz", 3))
    >>> m = MachineLearnModel(framework="sklearn", name="test",
    ...                       description="Machine learn model", path=path)
    >>> udf_data.append_machine_learn_model(m)
    >>> print(udf_data.get_feature_collection_by_id("C"))
    id: C
    start_times: None
    end_times: None
    data:    a  b         geometry
    0  1  a      POINT (0 0)
    1  2  b  POINT (100 100)
    2  3  c    POINT (100 0)
    >>> print(udf_data.get_feature_collection_by_id("D"))
    id: D
    start_times: None
    end_times: None
    data:    a  b         geometry
    0  1  a      POINT (0 0)
    1  2  b  POINT (100 100)
    2  3  c    POINT (100 0)
    >>> print(len(udf_data.get_feature_collection_list()) == 2)
    True
    >>> print(udf_data.ml_model_list[0].path)
    /tmp/test.pkl.xz
    >>> print(udf_data.ml_model_list[0].framework)
    sklearn

    >>> import json
    >>> json.dumps(udf_data.to_dict()) # doctest: +ELLIPSIS
    ...                                # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "user_context": {}, "server_context": {}, "datacubes": [], "feature_collection_list": [{"id": "C", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}, {"id": "D", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}], "structured_data_list": [], "machine_learn_models": [{"description": "Machine learn model", "name": "test", "framework": "sklearn", "path": "/tmp/test.pkl.xz", "md5_hash": null}]}'

    >>> udf = UdfData.from_dict(udf_data.to_dict())
    >>> json.dumps(udf.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "user_context": {}, "server_context": {}, "datacubes": [], "feature_collection_list": [{"id": "C", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}, {"id": "D", "data": {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"}, "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}}, {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"}, "geometry": {"type": "Point", "coordinates": [100.0, 100.0]}}, {"id": "2", "type": "Feature", "properties": {"a": 3, "b": "c"}, "geometry": {"type": "Point", "coordinates": [100.0, 0.0]}}]}}], "structured_data_list": [], "machine_learn_models": [{"description": "Machine learn model", "name": "test", "framework": "sklearn", "path": "/tmp/test.pkl.xz", "md5_hash": null}]}'

    >>> sd_list = StructuredData(description="Data list", data={"list":[1,2,3]}, type="list")
    >>> sd_dict = StructuredData(description="Data dict", data={"A":{"B": 1}}, type="dict")
    >>> udf = UdfData(proj={"EPSG":4326}, structured_data_list=[sd_list, sd_dict])
    >>> json.dumps(udf.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "user_context": {}, "server_context": {}, "datacubes": [], "feature_collection_list": [], "structured_data_list": [{"description": "Data list", "data": {"list": [1, 2, 3]}, "type": "list"}, {"description": "Data dict", "data": {"A": {"B": 1}}, "type": "dict"}], "machine_learn_models": []}'

    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)), coords={'x': [1, 2], 'y': [1, 2, 3]}, dims=('x', 'y'))
    >>> array.attrs["description"] = "This is an xarray with two dimensions"
    >>> array.name = "testdata"
    >>> h = DataCube(array=array)
    >>> udf_data = UdfData(proj={"EPSG":4326}, datacube_list=[h])
    >>> udf_data.user_context = {"kernel": 3}
    >>> udf_data.server_context = {"reduction_dimension": "t"}
    >>> udf_data.user_context
    {'kernel': 3}
    >>> udf_data.server_context
    {'reduction_dimension': 't'}
    >>> print(udf_data.get_datacube_by_id("testdata").to_dict())
    {'id': 'testdata', 'data': [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], 'dimensions': [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}], 'description': 'This is an xarray with two dimensions'}
    >>> json.dumps(udf_data.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "user_context": {"kernel": 3}, "server_context": {"reduction_dimension": "t"}, "datacubes": [{"id": "testdata", "data": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], "dimensions": [{"name": "x", "coordinates": [1, 2]}, {"name": "y", "coordinates": [1, 2, 3]}], "description": "This is an xarray with two dimensions"}], "feature_collection_list": [], "structured_data_list": [], "machine_learn_models": []}'

    >>> udf = UdfData.from_dict(udf_data.to_dict())
    >>> json.dumps(udf.to_dict()) # doctest: +ELLIPSIS
    ...                           # doctest: +NORMALIZE_WHITESPACE
    '{"proj": {"EPSG": 4326}, "user_context": {}, "server_context": {}, "datacubes": [{"id": "testdata", "data": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], "dimensions": [{"name": "x", "coordinates": [1, 2]}, {"name": "y", "coordinates": [1, 2, 3]}], "description": "This is an xarray with two dimensions"}], "feature_collection_list": [], "structured_data_list": [], "machine_learn_models": []}'

    """

    def __init__(self, proj: Dict,
                 datacube_list: Optional[List[DataCube]]=None,
                 feature_collection_list: Optional[List[FeatureCollection]]=None,
                 structured_data_list: Optional[List[StructuredData]]=None,
                 ml_model_list: Optional[List[MachineLearnModel]]=None):
        """The constructor of the UDF argument class that stores all data required by the
        user defined function.

        Args:
            proj (dict): A dictionary of form {"proj type string": "projection decription"} i. e. {"EPSG":4326}
            datacube_list (list(HyperCube)): A list of HyperCube objects
            feature_collection_list (list[FeatureCollection]): A list of VectorTile objects
            structured_data_list (list[StructuredData]): A list of structured data objects
            ml_model_list (list[MachineLearnModel]): A list of machine learn models
        """

        self._datacube_list = []
        self._feature_tile_list = []
        self._datacube_dict = {}
        self._feature_tile_dict = {}
        self._structured_data_list = []
        self._ml_model_list = []
        self.proj = proj

        self._user_context : Dict = dict()
        self._server_context : Dict = dict()

        if datacube_list:
            self.set_datacube_list(datacube_list=datacube_list)
        if feature_collection_list:
            self.set_feature_collection_list(feature_collection_list=feature_collection_list)
        if structured_data_list:
            self.set_structured_data_list(structured_data_list=structured_data_list)
        if ml_model_list:
            self.set_ml_model_list(ml_model_list=ml_model_list)

    @property
    def user_context(self) -> Dict:
        """Return the user context that was passed to the run_udf function"""
        return self._user_context

    @user_context.setter
    def user_context(self, context: Dict):
        """Set the user context"""
        self._user_context = context

    @property
    def server_context(self) -> Dict:
        """Return the server context that is passed from the backend to the UDF server for runtime configuration"""
        return self._server_context

    @server_context.setter
    def server_context(self, context: Dict):
        """Return the server context"""
        self._server_context = context

    def get_datacube_by_id(self, id: str) -> Optional[DataCube]:
        """Get a datacube by its id

        Args:
            id (str): The datacube id

        Returns:
            HypeCube: the requested datacube or None if not found

        """
        if id in self._datacube_dict:
            return self._datacube_dict[id]
        return None

    def get_feature_collection_by_id(self, id: str) -> Optional[FeatureCollection]:
        """Get a feature collection by its id

        Args:
            id (str): The vector tile id

        Returns:
            FeatureCollection: the requested feature collection or None if not found

        """
        if id in self._feature_tile_dict:
            return self._feature_tile_dict[id]
        return None

    def get_datacube_list(self) -> Optional[List[DataCube]]:
        """Get the datacube list
        """
        return self._datacube_list

    def set_datacube_list(self, datacube_list: List[DataCube]):
        """Set the datacube list

        If datacube_list is None, then the list will be cleared

        Args:
            datacube_list (List[DataCube]): A list of HyperCube's
        """

        self.del_datacube_list()
        if datacube_list is None:
            return

        for datacube in datacube_list:
            self.append_datacube(datacube)

    def del_datacube_list(self):
        """Delete all datacubes
        """
        self._datacube_list.clear()
        self._datacube_dict.clear()

    def get_feature_collection_list(self) -> Optional[List[FeatureCollection]]:
        """Get all feature collections as list

        Returns:
            list[FeatureCollection]: The list of feature collections

        """
        return self._feature_tile_list

    def set_feature_collection_list(self, feature_collection_list: Optional[List[FeatureCollection]]):
        """Set the feature collection tiles

        If feature_collection_tiles is None, then the list will be cleared

        Args:
            feature_collection_list (list[FeatureCollection]): A list of FeatureCollectionTile's
        """

        self.del_feature_collection_list()
        if feature_collection_list is None:
            return

        for entry in feature_collection_list:
            self.append_feature_collection(entry)

    def del_feature_collection_list(self):
        """Delete all feature collection tiles
        """
        self._feature_tile_list.clear()
        self._feature_tile_dict.clear()

    def get_structured_data_list(self) -> Optional[List[StructuredData]]:
        """Get all structured data entries

        Returns:
            (list[StructuredData]): A list of StructuredData objects

        """
        return self._structured_data_list

    def set_structured_data_list(self, structured_data_list: Optional[List[StructuredData]]):
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

    def get_ml_model_list(self) -> Optional[List[MachineLearnModel]]:
        """Get all machine learn models

        Returns:
            (list[MachineLearnModel]): A list of MachineLearnModel objects

        """
        return self._ml_model_list

    def set_ml_model_list(self, ml_model_list: Optional[List[MachineLearnModel]]):
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

    datacube_list = property(fget=get_datacube_list,
                             fset=set_datacube_list, fdel=del_datacube_list)
    feature_collection_list = property(fget=get_feature_collection_list,
                                       fset=set_feature_collection_list, fdel=del_feature_collection_list)
    structured_data_list = property(fget=get_structured_data_list,
                                    fset=set_structured_data_list, fdel=del_structured_data_list)
    ml_model_list = property(fget=get_ml_model_list,
                                  fset=set_ml_model_list, fdel=del_ml_model_list)


    def append_datacube(self, datacube: DataCube):
        """Append a HyperCube to the list

        It will be automatically added to the dictionary of all datacubes

        Args:
            datacube (DataCube): The HyperCube to append
        """
        self._datacube_list.append(datacube)
        self._datacube_dict[datacube.id] = datacube

    def append_feature_collection(self, feature_collection_tile: FeatureCollection):
        """Append a feature collection tile to the list

        It will be automatically added to the dictionary of all feature collection tiles

        Args:
            feature_collection_tile (FeatureCollection): The feature collection tile to append
        """
        self._feature_tile_list.append(feature_collection_tile)
        self._feature_tile_dict[feature_collection_tile.id] = feature_collection_tile

    def append_structured_data(self, structured_data: StructuredData):
        """Append a structured data object to the list

        Args:
            structured_data (StructuredData): A StructuredData objects
        """
        self._structured_data_list.append(structured_data)

    def append_machine_learn_model(self, machine_learn_model: MachineLearnModel):
        """Append a machine learn model to the list

        Args:
            machine_learn_model (MachineLearnModel): A MachineLearnModel objects
        """
        self._ml_model_list.append(machine_learn_model)

    def to_dict(self) -> Dict:
        """Convert this UdfData object into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            UdfData object as a dictionary
        """

        d = {"proj": self.proj, "user_context": self.user_context, "server_context": self.server_context}

        if self._datacube_list is not None:
            l = []
            for datacube in self._datacube_list:
                l.append(datacube.to_dict())
            d["datacubes"] = l

        if self._feature_tile_list is not None:
            l = []
            for tile in self._feature_tile_list:
                l.append(tile.to_dict())
            d["feature_collection_list"] = l

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
    def from_dict(udf_dict: Dict):
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

        if "user_context" in udf_dict:
            udf_data.user_context = udf_dict["user_context"]

        if "server_context" in udf_dict:
            udf_data.server_context = udf_dict["server_context"]

        if "datacubes" in udf_dict:
            l = udf_dict["datacubes"]
            for entry in l:
                h = DataCube.from_dict(entry)
                udf_data.append_datacube(h)

        if "feature_collection_list" in udf_dict:
            l = udf_dict["feature_collection_list"]
            for entry in l:
                fct = FeatureCollection.from_dict(entry)
                udf_data.append_feature_collection(fct)

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
