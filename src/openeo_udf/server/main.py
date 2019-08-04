# -*- coding: utf-8 -*-
import os
from openeo_udf.server.app import flask_app
from openeo_udf.server.endpoints import create_endpoints
from openeo_udf.server.config import UdfConfiguration


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"

create_endpoints()

if __name__ == '__main__':
    # Create the machine learn storage path
    if not os.path.isdir(UdfConfiguration.machine_learn_storage_path):
        os.mkdir(UdfConfiguration.machine_learn_storage_path)

    flask_app.run(host='0.0.0.0', port=8081, debug=True)
