# -*- coding: utf-8 -*-
from openeo_udf.server.app import flask_app
from openeo_udf.server.endpoints import create_endpoints


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"

create_endpoints()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8081, debug=True)
