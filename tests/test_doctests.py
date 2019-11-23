# -*- coding: utf-8 -*-
"""
Temporal framework doctests
"""

import doctest
import unittest
from openeo_udf.api import collection_base, feature_collection, hypercube, \
    machine_learn_model, spatial_extent, udf_data, structured_data


def load_tests(loader, tests, ignore):
    """Load all doctests from the base implementation as unittests"""
    tests.addTests(doctest.DocTestSuite(collection_base))
    tests.addTests(doctest.DocTestSuite(feature_collection))
    tests.addTests(doctest.DocTestSuite(hypercube))
    tests.addTests(doctest.DocTestSuite(machine_learn_model))
    tests.addTests(doctest.DocTestSuite(spatial_extent))
    tests.addTests(doctest.DocTestSuite(structured_data))
    tests.addTests(doctest.DocTestSuite(udf_data))
    return tests


if __name__ == '__main__':
    unittest.main()
