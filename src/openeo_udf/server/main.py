# -*- coding: utf-8 -*-
from openeo_udf.server.app import app
from openeo_udf.server.endpoints import create_storage_directory
import openeo_udf.server.udf
import openeo_udf.server.machine_learn_database

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"

create_storage_directory()

