# -*- coding: utf-8 -*-
from pprint import pprint
from typing import List

import unittest
from hashlib import md5
from openeo_udf.server.app import app
from starlette.testclient import TestClient

from openeo_udf.server.tools import create_storage_directory
from openeo_udf.server.machine_learn_database import RequestStorageModel, ResponseStorageModel

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"



class MachineLearningModelStorageTestCase(unittest.TestCase):

    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    def test_ml_storage_post_get_delete(self):

        path = "/tmp/test_file"
        content = b"content"

        # Create a dummy file
        file = open(path, "wb")
        file.write(content)
        file.close()

        request_model = RequestStorageModel(uri=path, title="This is a test model",
                                            description="This is the test description.")

        response = self.app.post('/storage', json=request_model.dict())
        print(response.content)
        self.assertEqual(response.status_code, 200)

        md5_hash = response.content.decode("ascii")
        self.assertEqual(md5_hash,  md5(content).hexdigest())

        response = self.app.get('/storage')
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

        response = self.app.delete(f'/storage/{md5_hash}')
        print(response.content)
        self.assertEqual(response.status_code, 200)

        md5_hash = response.content.decode("ascii")
        self.assertEqual(md5_hash,  md5(content).hexdigest())

    def test_ml_storage_post_get_delete_url(self):

        url = "https://storage.googleapis.com/datentransfer/europe_countries.geojson"

        request_model = RequestStorageModel(uri=url, title="This is a test model",
                                            description="This is the test description.")

        response = self.app.post('/storage', json=request_model.dict())
        print(response.content)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/storage')
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

        md5_hash = None

        model_list: List[dict] = response.json()
        for model in model_list:

            model = ResponseStorageModel(**model)
            if model.source == url:
                md5_hash = model.md5_hash

        self.assertIsNotNone(md5_hash)

        response = self.app.delete(f'/storage/{md5_hash}')
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_ml_storage_post_url_error(self):

        url = "https://nopopopop.de/file.txt"

        request_model = RequestStorageModel(uri=url, title="This is a test model",
                                            description="This is the test description.")

        response = self.app.post('/storage', json=request_model.dict())
        # pprint(response.json())
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
