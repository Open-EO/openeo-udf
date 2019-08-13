# -*- coding: utf-8 -*-
import base64
from copy import deepcopy

import msgpack
import os
import pprint
import unittest

from openeo_udf.server.machine_learn_database import RequestStorageModel

from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfCodeModel, UdfRequestModel
import openeo_udf.functions
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
import pandas as pd
from sklearn.externals import joblib

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PIXEL = {
    "proj": {"EPSG":4326},
    "raster_collection_tiles": [
        {
            "id": "RED",
            "wavelength": 420,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00"],
            "data": [[[1, 2]],
                     [[3, 2]]],
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
            "data": [[[2, 1]],
                     [[2, 3]]],
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
    "machine_learn_models": [
        {"framework": "sklearn",
         "name": "random_forest",
         "description": "A sklearn model that adds two numbers in range of [1,3]",
         "path": "/tmp/rf_add_model.pkl.xz"
         }
    ]
}


class MachineLearningTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app)

    @staticmethod
    def compute_efficiency(model_result, measurement):
        diff = model_result - measurement
        eff = 1 - sum(diff * diff) / ((measurement.var()) * len(measurement))
        return (eff)

    @staticmethod
    def train_sklearn_model(model):
        """This method trains a sklearn random forest regressor to add two numbers that must be
        in range [1,2,3]. The input arrays into the model must have the names *red* and *nir*.

        Args:
            model: The machine learn model to be used for training

        Returns:
            str:
            The filename of the resulting

        """

        # Train a value adder that represents the formula (a + b)
        a = np.random.randint(1, 4, 1000)
        b = np.random.randint(1, 4, 1000)
        # Create the predicting data that is used for training
        y = (a + b)

        print("Train model ", model.__class__)
        # This is the training data with two arrays
        X = pd.DataFrame()

        X["red"] = a
        X["nir"] = b

        # Fit the model and compute the model efficiency
        model = model.fit(X, y)
        # Predict values
        predicted_values = model.predict(X)
        # Compute the score of the model
        score = model.score(X, y)
        # Compute the mean square error
        mse = mean_squared_error(predicted_values, y)

        print("Model score", score, "MSE", mse)
        print("Save the model as compressed joblib object")

        # Save the model with compression
        file_name = '/tmp/rf_add_model.pkl.xz'
        joblib.dump(value=model, filename=file_name, compress=("xz", 3))
        return file_name

    def test_sklearn_random_forest(self):
        """Test random forest model training and UDF application"""
        model = RandomForestRegressor(n_estimators=100, max_depth=7,
                                      max_features="log2", n_jobs=16,
                                      min_samples_split=2,
                                      min_samples_leaf=1,
                                      verbose=0)

        MachineLearningTestCase.train_sklearn_model(model=model)
        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL
        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[3.0, 3.0]], [[5.0, 5.0]]])

    def test_sklearn_random_forest_message_pack(self):
        """Test random forest model training and UDF application"""
        model = RandomForestRegressor(n_estimators=100, max_depth=7,
                                      max_features="log2", n_jobs=16,
                                      min_samples_split=2,
                                      min_samples_leaf=1,
                                      verbose=0)

        MachineLearningTestCase.train_sklearn_model(model=model)
        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        udf_request = base64.b64encode(msgpack.packb(udf_request.dict(), use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request,
                                 headers={"Content-Type":"application/base64"})
        self.assertEqual(response.status_code, 200)
        blob = base64.b64decode(response.content)
        result = msgpack.unpackb(blob, raw=False)

        self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[3.0, 3.0]], [[5.0, 5.0]]])

    def otest_sklearn_gradient_boost(self):
        """Test gradent boost model training and UDF application"""
        model = GradientBoostingRegressor(n_estimators=100, max_depth=7,
                                          max_features="log2",
                                          min_samples_split=2,
                                          min_samples_leaf=1,
                                          verbose=0)
        MachineLearningTestCase.train_sklearn_model(model=model)
        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL
        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()
        pprint.pprint(result)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][0][0][0], 3.0, 2)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][1][0][0], 5.0, 2)

    def test_sklearn_gradient_boost_message_pack(self):
        """Test gradent boost model training and UDF application"""
        model = GradientBoostingRegressor(n_estimators=100, max_depth=7,
                                          max_features="log2",
                                          min_samples_split=2,
                                          min_samples_leaf=1,
                                          verbose=0)
        MachineLearningTestCase.train_sklearn_model(model=model)
        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        udf_request = base64.b64encode(msgpack.packb(udf_request.dict(), use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request,
                                 headers={"Content-Type":"application/base64"})
        self.assertEqual(response.status_code, 200)
        blob = base64.b64decode(response.content)
        result = msgpack.unpackb(blob, raw=False)

        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][0][0][0], 3.0, 2)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][1][0][0], 5.0, 2)

    def test_sklearn_extra_tree(self):
        """Test extra tree training and UDF application"""
        model = ExtraTreesRegressor(n_estimators=100, max_depth=7,
                                    max_features="log2",
                                    min_samples_split=2,
                                    min_samples_leaf=1,
                                    verbose=0)
        MachineLearningTestCase.train_sklearn_model(model=model)
        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL
        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        self.assertEqual(response.status_code, 200)
        result = response.json()
        pprint.pprint(result)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][0][0][0], 3.0, 2)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][1][0][0], 5.0, 2)

    def test_sklearn_extra_tree_message_pack(self):
        """Test extra tree training and UDF application with message pack protocol"""
        model = ExtraTreesRegressor(n_estimators=100, max_depth=7,
                                    max_features="log2",
                                    min_samples_split=2,
                                    min_samples_leaf=1,
                                    verbose=0)
        MachineLearningTestCase.train_sklearn_model(model=model)
        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        udf_request = base64.b64encode(msgpack.packb(udf_request.dict(), use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request,
                                 headers={"Content-Type":"application/base64"})
        self.assertEqual(response.status_code, 200)
        blob = base64.b64decode(response.content)
        result = msgpack.unpackb(blob, raw=False)

        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][0][0][0], 3.0, 2)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][1][0][0], 5.0, 2)

    def test_sklearn_extra_tree_message_pack_md5_hash(self):
        """Test extra tree training and UDF application with message pack protocol and the machine learn model
        uploaded to the UDF md5 hash based storage system"""
        model = ExtraTreesRegressor(n_estimators=100, max_depth=7,
                                    max_features="log2",
                                    min_samples_split=2,
                                    min_samples_leaf=1,
                                    verbose=0)
        model_path = MachineLearningTestCase.train_sklearn_model(model=model)

        request_model = RequestStorageModel(uri=model_path, title="This is a test model",
                                            description="This is the test description.")

        response = self.app.post('/storage', json=request_model.dict())
        print(response.content)
        self.assertEqual(response.status_code, 200)

        md5_hash = response.content.decode("ascii").strip().replace("\"", "")

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_sklearn_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())
        udf_data = deepcopy(PIXEL)
        udf_data["machine_learn_models"][0]["md5_hash"] = md5_hash

        udf_request = UdfRequestModel(data=udf_data, code=udf_code)
        udf_request = base64.b64encode(msgpack.packb(udf_request.dict(), use_bin_type=True))
        response = self.app.post('/udf_message_pack', data=udf_request,
                                 headers={"Content-Type":"application/base64"})
        self.assertEqual(response.status_code, 200)
        blob = base64.b64decode(response.content)
        result = msgpack.unpackb(blob, raw=False)

        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][0][0][0], 3.0, 2)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][1][0][0], 5.0, 2)

        response = self.app.delete(f'/storage/{md5_hash}')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
