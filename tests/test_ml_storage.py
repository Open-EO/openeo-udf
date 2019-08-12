# -*- coding: utf-8 -*-
from pprint import pprint

from flask import json
import unittest
from hashlib import md5
from openeo_udf.server.main import app
from starlette.testclient import TestClient

from openeo_udf.server.endpoints import create_storage_directory

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

        response = self.app.post('/storage', data=path, headers={"Content-Type": "text/plain"})
        #print(response.content)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/storage')
        #print(response.content)
        self.assertEqual(response.status_code, 200)

        md5_hash = md5(content).hexdigest()
        #print(response.content)
        response = self.app.delete(f'/storage/{md5_hash}')
        self.assertEqual(response.status_code, 200)

    def test_ml_storage_post_get_delete_url(self):

        url = "https://storage.googleapis.com/datentransfer/europe_countries.geojson"

        response = self.app.post('/storage', data=url, headers={"Content-Type": "text/plain"})
        #print(response.content)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/storage')
        #print(response.content)
        self.assertEqual(response.status_code, 200)

        md5_hash = response.json()[0]

        response = self.app.delete(f'/storage/{md5_hash}')
        #print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_ml_storage_post_url_error(self):

        url = "https://nopopopop.de/file.txt"

        response = self.app.post('/storage', data=url, headers={"Content-Type": "text/plain"})
        # pprint(response.json())
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
