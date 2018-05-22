# -*- coding: utf-8 -*-
"""
Temporal framework doctests
"""

import doctest
import unittest
from openeo_udf.api import base


def load_tests(loader, tests, ignore):
    """Load all doctests from the base implementation as unittests"""
    tests.addTests(doctest.DocTestSuite(base))
    return tests


if __name__ == '__main__':
    unittest.main()
