# -*- coding: utf-8 -*-
import os
from openeo_udf.server.config import UdfConfiguration
from openeo_udf.server.app import flask_api
from openeo_udf.server.udf import Udf, UdfMessagePack
from openeo_udf.server.machine_learn_database import MachineLearnDatabase

__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"

created = False


def create_endpoints():
    """Create all endpoints for the openEO UDF API

    :return:
    """
    global created

    # Create the machine learn storage path
    if not os.path.isdir(UdfConfiguration.machine_learn_storage_path):
        os.mkdir(UdfConfiguration.machine_learn_storage_path)

    if created is False:
        flask_api.add_resource(Udf, '/udf')
        flask_api.add_resource(UdfMessagePack, '/udf_message_pack')
        flask_api.add_resource(MachineLearnDatabase, '/ml_storage')
        created = True

