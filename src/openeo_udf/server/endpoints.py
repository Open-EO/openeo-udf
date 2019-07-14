# -*- coding: utf-8 -*-
from .app import flask_api
from .udf import Udf, UdfMessagePack

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

    if created is False:
        flask_api.add_resource(Udf, '/udf')
        flask_api.add_resource(UdfMessagePack, '/udf_message_pack')
        created = True

