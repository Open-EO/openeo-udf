# -*- coding: utf-8 -*-
from flask import json

import pprint
import sys
import unittest
from openeo_udf.server.app import flask_api
from openeo_udf.server.endpoints import create_endpoints
from openeo_udf.server.definitions import UdfData, UdfCode, UdfRequest
from openeo_udf.api.base import SpatialExtent, RasterCollectionTile, FeatureCollectionTile

import numpy
import pandas
import torch
import torchvision
import tensorflow
import tensorboard

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PIXEL={
        "proj": "EPSG:4326",
        "raster_collection_tiles": [
            {
                "id": "RED",
                "wavelength": 420,
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": [[[5, 4]],
                         [[9, 10]]],
                "extent": {
                    "top": 53,
                    "bottom": 51,
                    "right": 30,
                    "left": 28,
                    "hight": 1,
                    "width": 1
                }
            },
            {
                "id": "GREEN",
                "wavelength": 340,
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": [[[3, 4]],
                         [[9, 8]]],
                "extent": {
                    "top": 53,
                    "bottom": 51,
                    "right": 30,
                    "left": 28,
                    "hight": 1,
                    "width": 1
                }
            }
        ]
    }

FEATURE={
        "proj": "EPSG:4326",
        "feature_collection_tiles": [
            {
                "id": "test_data",
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                                       "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}},
                                      {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                                       "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
                         "type": "FeatureCollection"}
            }
        ]
    }

PIXEL_FEATURE={
        "proj": "EPSG:4326",
        "raster_collection_tiles": [

            {
                "id": "RED",
                "wavelength": 420,
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": [[[5, 4]],
                         [[9, 10]]],
                "extent": {
                    "top": 53,
                    "bottom": 51,
                    "right": 30,
                    "left": 28,
                    "hight": 1,
                    "width": 1
                }
            },
            {
                "id": "GREEN",
                "wavelength": 340,
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": [[[3, 4]],
                         [[9, 8]]],
                "extent": {
                    "top": 53,
                    "bottom": 51,
                    "right": 30,
                    "left": 28,
                    "hight": 1,
                    "width": 1
                }
            }
        ],
        "feature_collection_tiles": [
            {
                "id": "test_data",
                "start_times": ["2001-01-01T00:00:00",
                                "2001-01-02T00:00:00"],
                "end_times": ["2001-01-02T00:00:00",
                              "2001-01-03T00:00:00"],
                "data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                                       "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}},
                                      {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                                       "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
                         "type": "FeatureCollection"}
            }
        ]
    }


CODE_SUM="""
def ict_time_sum(udf_data):
    tile_results = []
    for tile in udf_data.raster_collection_tiles:
        tile_sum = numpy.sum(tile.data, axis=0)
        rows, cols = tile_sum.shape
        array3d = numpy.ndarray([1, rows, cols])
        array3d[0] = tile_sum
        
        starts = pandas.DatetimeIndex([tile.start_times[0]])
        ends = pandas.DatetimeIndex([tile.end_times[-1]])
        
        ict = RasterCollectionTile(id=tile.id + "_sum", extent=tile.extent, data=array3d, start_times=starts, end_times=ends)
        tile_results.append(ict)
    udf_data.set_raster_collection_tiles(tile_results)

ict_time_sum(data)

"""

CODE_MIN_MEAN_MAX_SUM = """
def ict_min_mean_max_sum(udf_data):
    tile_results = []
    for tile in udf_data.raster_collection_tiles:
        tile_min  = numpy.min(tile.data, axis=0)
        tile_mean = numpy.mean(tile.data, axis=0)
        tile_max  = numpy.max(tile.data, axis=0)
        tile_sum  = numpy.sum(tile.data, axis=0)
        rows, cols = tile_sum.shape
        array3d_min  = numpy.ndarray([1, rows, cols])
        array3d_mean = numpy.ndarray([1, rows, cols])
        array3d_max  = numpy.ndarray([1, rows, cols])
        array3d_sum  = numpy.ndarray([1, rows, cols])
        array3d_min[0]  = tile_min
        array3d_mean[0] = tile_mean
        array3d_max[0]  = tile_max
        array3d_sum[0]  = tile_sum

        starts = pandas.DatetimeIndex([tile.start_times[0]])
        ends = pandas.DatetimeIndex([tile.end_times[-1]])

        ict = RasterCollectionTile(id=tile.id + "_min", extent=tile.extent, data=array3d_min, start_times=starts, end_times=ends)
        tile_results.append(ict)
        ict = RasterCollectionTile(id=tile.id + "_mean", extent=tile.extent, data=array3d_mean, start_times=starts, end_times=ends)
        tile_results.append(ict)
        ict = RasterCollectionTile(id=tile.id + "_max", extent=tile.extent, data=array3d_max, start_times=starts, end_times=ends)
        tile_results.append(ict)
        ict = RasterCollectionTile(id=tile.id + "_sum", extent=tile.extent, data=array3d_sum, start_times=starts, end_times=ends)
        tile_results.append(ict)
    udf_data.set_raster_collection_tiles(tile_results)

ict_min_mean_max_sum(data)

"""


class AllTestCase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()

    def test_pixel_sum(self):

        udf_data = PIXEL
        udf_code = UdfCode(language="python", source=CODE_SUM)

        udf_request = UdfRequest(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

    def test_pixel_min_mean_max_sum(self):

        udf_data = PIXEL
        udf_code = UdfCode(language="python", source=CODE_MIN_MEAN_MAX_SUM)

        udf_request = UdfRequest(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)


if __name__ == "__main__":
    unittest.main()
