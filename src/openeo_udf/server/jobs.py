# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import abort, Resource
from flask_restful_swagger_2 import swagger
from .definitions import UdfProcess

__license__ = "Apache License, Version 2.0"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__      = "soerengebbert@googlemail.com"


POST_JOBS_EXAMPLE = {"job_id": "42d5k3nd92mk49dmj294md"}

POST_JOBS_DOC = {
    "summary": "submits a new job to the back-end",
    "description": "creates a new job from one or more (chained) processes at the back-end, "
                   "which will eventually run the computations",
    "tags": ["Job Management"],
    "parameters": [
        {
            "name": "evaluate",
            "in": "query",
            "description": "Defines how the job should be evaluated. Can be `lazy` (the default), `batch`, or "
                           "`sync` where lazy means that the job runs computations only on download requests "
                           "considering dynamically provided views. Batch jobs are immediately scheduled for "
                           "execution by the back-end. Synchronous jobs will be immediately executed and return "
                           "the result data.",
            "type": "string",
            "enum": ["lazy", "batch", "sync"],
            "default": "lazy",
            "required": False
        },
        {
            "name": "process_graph",
            "in": "body",
            "description": "Description of one or more (chained) processes including their input arguments",
            "schema": UdfProcess
        },
        {
            "name": "format",
            "in": "query",
            "description": "Description of the desired output format. Required in case `evaluate` is set to `sync`. "
                           "If not specified the format has to be specified in the download request.",
            "type": "string",
            "enum": ["nc", "json", "wcs", "wmts", "tms", "tif", "png", "jpeg"],
            "required": False
        }
    ],
    "responses": {
        "200": {
            "description": "Depending on the job evaluation type, the result of posting jobs can be either a json "
                           "description of the job (for lazy and batch jobs) or a result object such as a NetCDF "
                           "file (for sync jobs).",
            "examples": {
                "application/json": POST_JOBS_EXAMPLE
            }
        },
        "406": {"description": "The server is not capable to deliver the requested format."},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class Jobs(Resource):
    @swagger.doc(POST_JOBS_DOC)
    def post(self, ):
        return make_response(jsonify(POST_JOBS_EXAMPLE), 200)
