# -*- coding: utf-8 -*-
from .app import flask_api
from .jobs import Jobs

__license__ = "Apache License, Version 2.0"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__      = "soerengebbert@googlemail.com"


def create_endpoints():
    """Create all endpoints for the openEO UDF API

    :return:
    """
    flask_api.add_resource(Jobs, '/jobs')


