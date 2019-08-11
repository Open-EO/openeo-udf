# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class StructuredDataSchema(Schema):
    description = "This model represents structured data that can not be represented" \
                  "as a RasterCollectionTile or FeatureCollectionTile. For example the result of a statistical " \
                  "computation. The data is self descriptive and supports the basic types dict/map, list and table. " \
                  "This data structure can also be used to provide contextual data from the user to the UDF, like " \
                  "kernel size, resampling pixel size and so on."
    type = "object"
    required = ["description", "data", "type"]
    properties = {
        "description": {
            "type": "string",
            "description": "A detailed description of the output format.",
        },
        "data": {
            "type": dict(),
            "description": "The structured data. This field contains the UDF specific values (argument or return)"
                           "as dict, list or table. "
                           "  * A dict can be as complex as required by the UDF."
                           "  * A list must contain simple data types example {\"list\": [1,2,3,4]} "
                           "  * A table is a list of lists with a header, example {\"table\": [[\"id\",\"value\"],"
                           "                                                                     [1,     10],"
                           "                                                                     [2,     23],"
                           "                                                                     [3,     4]]}"
        },
        "type": {
            "type": "string",
            "description": "The type of the structured data that may be of type dict, table or list. "
                           "This is just a hint for the user how to interpret the provided data.",
            "enum": ["dict", "table", "list"]
        }
    }
    example = {"description": "Output of a statistical analysis. The univariate analysis "
                              "of multiple raster collection tiles. Each entry in the output dict/map contains "
                              "min, mean and max of all pixels in a raster collection tile. The key "
                              "is the id of the raster collection tile.",
               "data": {"RED":{"min":0, "max":100, "mean":50}, "NIR":{"min":0, "max":100, "mean":50}},
               "type": "dict"}
