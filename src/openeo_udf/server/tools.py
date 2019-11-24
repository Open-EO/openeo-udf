# -*- coding: utf-8 -*-
import os
from openeo_udf.server.config import UdfConfiguration

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

created = False


def create_storage_directory():
    """Create all endpoints for the openEO UDF API

    :return:
    """
    global created

    # Create the machine learn storage path
    if not os.path.isdir(UdfConfiguration.machine_learn_storage_path):
        os.mkdir(UdfConfiguration.machine_learn_storage_path)
