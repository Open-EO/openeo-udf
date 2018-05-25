# -*- coding: utf-8 -*-
from flask import json
import os
import pprint
import unittest
from openeo_udf.server.app import flask_api
from openeo_udf.server.endpoints import create_endpoints
from openeo_udf.server.definitions import UdfData, UdfCode, UdfRequest
import openeo_udf.functions


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
                "id": "NIR",
                "wavelength": 670,
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
                "id": "NIR",
                "wavelength": 670,
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


class AllTestCase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()

    def test_pixel_sum(self):
        """Test the time reduce sum UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_reduce_time_sum.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequest(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["raster_collection_tiles"]), 2)
        self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[14.0, 14.0]]])
        self.assertEqual(result["raster_collection_tiles"][1]["data"], [[[12.0, 12.0]]])

    def test_pixel_min_mean_max_sum(self):
        """Test the time reduce min, max, mean, sum UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_reduce_time_min_max_mean_sum.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequest(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["raster_collection_tiles"]), 8)
        self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[5.0, 4.0]]])
        self.assertEqual(result["raster_collection_tiles"][1]["data"], [[[9.0, 10.0]]])
        self.assertEqual(result["raster_collection_tiles"][2]["data"], [[[14.0, 14.0]]])
        self.assertEqual(result["raster_collection_tiles"][3]["data"], [[[7.0, 7.0]]])
        self.assertEqual(result["raster_collection_tiles"][4]["data"], [[[3.0, 4.0]]])
        self.assertEqual(result["raster_collection_tiles"][5]["data"], [[[9.0, 8.0]]])
        self.assertEqual(result["raster_collection_tiles"][6]["data"], [[[12.0, 12.0]]])
        self.assertEqual(result["raster_collection_tiles"][7]["data"], [[[6.0, 6.0]]])

    def test_ndvi(self):
        """Test the time reduce sum UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_ndvi.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequest(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["raster_collection_tiles"]), 1)
        self.assertEqual(result["raster_collection_tiles"][0]["data"],
                         [[[-0.25, 0.0]], [[0.0, -0.1111111111111111]]])

    def test_buffer(self):
        """Test the time reduce sum UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "feature_collections_buffer.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = FEATURE

        udf_request = UdfRequest(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["feature_collection_tiles"]), 1)
        self.assertEqual(len(result["feature_collection_tiles"][0]["data"]["features"]), 2)
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][0]["properties"], {'a': 1, 'b': 'a'})
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][1]["properties"], {'a': 2, 'b': 'b'})


if __name__ == "__main__":
    unittest.main()
