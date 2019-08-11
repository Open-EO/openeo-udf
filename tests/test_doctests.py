# -*- coding: utf-8 -*-
"""
Temporal framework doctests
"""

import doctest
import unittest
from openeo_udf.api import collection_tile, feature_collection_tile, hypercube, machine_learn_model, spatial_extent, udf_data


def load_tests(loader, tests, ignore):
    """Load all doctests from the base implementation as unittests"""
    tests.addTests(doctest.DocTestSuite(collection_tile))
    tests.addTests(doctest.DocTestSuite(feature_collection_tile))
    tests.addTests(doctest.DocTestSuite(hypercube))
    tests.addTests(doctest.DocTestSuite(machine_learn_model))
    tests.addTests(doctest.DocTestSuite(spatial_extent))
    tests.addTests(doctest.DocTestSuite(udf_data))
    return tests


if __name__ == '__main__':
    unittest.main()
