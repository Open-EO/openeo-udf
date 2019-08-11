#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class CustomUdfParameter(dict):
    """This class represent custom UDF parameter that the user can set for the provided UDF code.
    The parameter must be provided as key - value entries in this class, which is a derivative of
    a dictionary


    >>> custom_params = CustomUdfParameter(kernel_size=3, time_delta=0.5)
    >>> custom_params["kernel_size"]
    3
    >>> custom_params["time_delta"]
    0.5

    """
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
