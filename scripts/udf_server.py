# -*- coding: utf-8 -*-
import argparse
from openeo_udf.server.app import flask_app
from openeo_udf.server.endpoints import create_endpoints

__license__ = "Apache License, Version 2.0"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__      = "soerengebbert@googlemail.com"


def main():

    parser = argparse.ArgumentParser(description='Start udf server')

    parser.add_argument("--host", type=str, required=False, default="0.0.0.0",
                        help="The IP address that should be used for the server")

    parser.add_argument("--port", type=int, required=False, default=5000,
                        help="The port that should be used for the server")

    parser.add_argument("--debug", type=bool, required=False, default=True,
                        help="Set True to activate debugging")

    args = parser.parse_args()


    create_endpoints()
    flask_app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
