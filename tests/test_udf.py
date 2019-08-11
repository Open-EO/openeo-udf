# -*- coding: utf-8 -*-
from flask import json
import os
import pprint
import unittest

from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfDataModel, UdfCodeModel, UdfRequestModel
import openeo_udf.functions

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PIXEL = {
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
                "height": 1,
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
                "height": 1,
                "width": 1
            }
        }
    ]
}

FEATURE = {
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

PIXEL_FEATURE = {
    "proj": "EPSG:4326",
    "raster_collection_tiles": [

        {
            "id": "RED",
            "wavelength": 420,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00"],
            "data": [[[5, 4],
                      [3, 2]],
                     [[9, 10],
                      [8, 9]]],
            "extent": {
                "top": 53,
                "bottom": 51,
                "right": 30,
                "left": 28,
                "height": 1,
                "width": 1
            }
        },
        {
            "id": "NIR",
            "wavelength": 670,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00",
                            "2001-01-03T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00",
                          "2001-01-04T00:00:00"],
            "data": [[[2, 1],
                      [4, 3]],
                     [[7, 8],
                      [6, 7]],
                     [[1, 0],
                      [1, 0]]],
            "extent": {
                "top": 53,
                "bottom": 51,
                "right": 30,
                "left": 28,
                "height": 1,
                "width": 1
            }
        }
    ],
    "feature_collection_tiles": [
        {
            "id": "test_data",
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00",
                            "2001-01-03T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00",
                          "2001-01-04T00:00:00"],
            "data": {"features": [{"id": "0", "type": "Feature", "properties": {},
                                   "geometry": {"coordinates": [28.5, 51.5], "type": "Point"}},
                                  {"id": "1", "type": "Feature", "properties": {},
                                   "geometry": {"coordinates": [29.5, 52.5], "type": "Point"}},
                                  {"id": "2", "type": "Feature", "properties": {},
                                   "geometry": {"coordinates": [25, 55], "type": "Point"}}],
                     "type": "FeatureCollection"}
        }
    ]
}


class AllTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_pixel_median(self):
        """Test the time reduce sum UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_reduce_time_median.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["raster_collection_tiles"]), 2)
        self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[7.0, 7.0]]])
        self.assertEqual(result["raster_collection_tiles"][1]["data"], [[[6.0, 6.0]]])

    def test_pixel_sum(self):
        """Test the time reduce sum UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_reduce_time_sum.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
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
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
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
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["raster_collection_tiles"]), 1)
        self.assertEqual(result["raster_collection_tiles"][0]["data"],
                         [[[-0.25, 0.0]], [[0.0, -0.1111111111111111]]])

    def test_buffer(self):
        """Test the feature collection buffering UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "feature_collections_buffer.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = FEATURE

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["feature_collection_tiles"]), 1)
        self.assertEqual(len(result["feature_collection_tiles"][0]["data"]["features"]), 2)
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][0]["properties"], {'a': 1, 'b': 'a'})
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][1]["properties"], {'a': 2, 'b': 'b'})

    def test_sampling(self):
        """Test the feature collection sampling UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sampling.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL_FEATURE

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["feature_collection_tiles"]), 1)
        self.assertEqual(len(result["feature_collection_tiles"][0]["data"]["features"]), 3)
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][0]["properties"], {'NIR_0': 4,
                                                                                                      'NIR_1': 6,
                                                                                                      "NIR_2": 1,
                                                                                                      "RED_0": 3,
                                                                                                      "RED_1": 8})
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][1]["properties"], {'NIR_0': 1,
                                                                                                      'NIR_1': 8,
                                                                                                      "NIR_2": 0,
                                                                                                      "RED_0": 4,
                                                                                                      "RED_1": 10})
        self.assertEqual(result["feature_collection_tiles"][0]["data"]["features"][2]["properties"], {'NIR_0': None,
                                                                                                      'NIR_1': None,
                                                                                                      "NIR_2": None,
                                                                                                      "RED_0": None,
                                                                                                      "RED_1": None})

    def test_rct_stats(self):
        """Test the raster collection tile statistics UDF"""

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_statistics.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        print(udf_request)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(len(result["feature_collection_tiles"]), 0)
        self.assertEqual(len(result["raster_collection_tiles"]), 0)
        self.assertEqual(len(result["structured_data_list"]), 1)
        self.assertEqual(result["structured_data_list"][0]["type"], "dict")
        self.assertEqual(result["structured_data_list"][0]["data"]["NIR"], {'max': 9.0, 'mean': 6.0,
                                                                            'min': 3.0, 'sum': 24.0})
        self.assertEqual(result["structured_data_list"][0]["data"]["RED"], {'max': 10.0, 'mean': 7.0,
                                                                            'min': 4.0, 'sum': 28.0})


if __name__ == "__main__":
    unittest.main()
