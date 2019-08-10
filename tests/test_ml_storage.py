# -*- coding: utf-8 -*-
from flask import json
import unittest
from hashlib import md5
from openeo_udf.server.app import flask_api
from openeo_udf.server.endpoints import create_endpoints

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"



class MachineLearningModelStorageTestCase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()

    def test_ml_storage_post_get_delete(self):

        path = "/tmp/test_file"
        content = b"content"

        # Create a dummy file
        file = open(path, "wb")
        file.write(content)
        file.close()

        response = self.app.post('/ml_storage', data=path, content_type="application/text")
        print(response.data)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/ml_storage')
        print(response.data)
        self.assertEqual(response.status_code, 200)

        md5_hash = md5(content).hexdigest()
        response = self.app.delete('/ml_storage', data=md5_hash, content_type="application/text")
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_ml_storage_post_get_delete_url(self):

        url = "https://storage.googleapis.com/datentransfer/europe_countries.geojson"

        response = self.app.post('/ml_storage', data=url, content_type="application/text")
        print(response.data)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/ml_storage')
        print(response.data)
        self.assertEqual(response.status_code, 200)

        md5_hash = json.loads(response.data)[0]

        response = self.app.delete('/ml_storage', data=md5_hash, content_type="application/text")
        print(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
