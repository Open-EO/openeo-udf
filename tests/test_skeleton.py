#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from openeo_udf_development.skeleton import fib

__author__ = "Soeren Gebbert"
__copyright__ = "Soeren Gebbert"
__license__ = "apache"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
