# -*- coding: utf-8 -*-
from flask import json
import os
import pprint
import unittest
from openeo_udf.server.app import flask_api
from openeo_udf.server.endpoints import create_endpoints
from openeo_udf.server.definitions import UdfData, UdfCode, UdfRequest
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
    "proj": "EPSG:4326",
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
         "description": "A random forest model that adds two numbers in range of [1,3]",
         "path": "/tmp/rf_add_model.pkl.xz"
         }
    ]
}


class MachineLearningTestCase(unittest.TestCase):
    create_endpoints()

    @staticmethod
    def compute_efficiency(model_result, measurement):
        diff = model_result - measurement
        eff = 1 - sum(diff * diff) / ((measurement.var()) * len(measurement))
        return (eff)

    def setUp(self):
        self.app = flask_api.app.test_client()

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
        file_name = os.path.join(dir, "raster_collections_ml.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequest(data=udf_data, code=udf_code)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[3.0, 3.0]], [[5.0, 5.0]]])

    def test_sklearn_gradient_boost(self):
        """Test gradent boost model training and UDF application"""

        model = GradientBoostingRegressor(n_estimators=100, max_depth=7,
                                          max_features="log2",
                                          min_samples_split=2,
                                          min_samples_leaf=1,
                                          verbose=0)

        MachineLearningTestCase.train_sklearn_model(model=model)

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "raster_collections_ml.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequest(data=udf_data, code=udf_code)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        # self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[3.0, 3.0]], [[5.0, 5.0]]])
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
        file_name = os.path.join(dir, "raster_collections_ml.py")
        udf_code = UdfCode(language="python", source=open(file_name, "r").read())
        udf_data = PIXEL

        udf_request = UdfRequest(data=udf_data, code=udf_code)

        response = self.app.post('/udf', data=json.dumps(udf_request), content_type="application/json")
        result = json.loads(response.data)
        pprint.pprint(result)

        # self.assertEqual(result["raster_collection_tiles"][0]["data"], [[[3.0, 3.0]], [[5.0, 5.0]]])
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][0][0][0], 3.0, 2)
        self.assertAlmostEqual(result["raster_collection_tiles"][0]["data"][1][0][0], 5.0, 2)


if __name__ == "__main__":
    unittest.main()
