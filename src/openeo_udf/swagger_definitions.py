#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Swagger UDF interface descriptions

"""

__license__ = "Apache License, Version 2.0"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__      = "soerengebbert@googlemail.com"

ITC_DOC = {
    "image_collection_tile": {
        "description": "A chunk of data that represents a spatio-temporal subset of a spatio-temporal dataset. "
                       "The approach to implement these data types can be different between the programming "
                       "languages.",
        "type": "object",
        "required": ["data", "id", "extent"],
        "properties": {
            "id": {
                "description": "The identifier of this image collection tile.",
                "type": "string"
            },
            "data": {
                "description": "A three dimensional array fo integer (8,16,32,64 bit) or float (16, 32, 64 bit) values."
                               "The index dimension is as follows: [time][y][x]. Hence, the index data[0] returns "
                               "the 2D slice for the first time-stamp. The y-indexing if counted from top to bottom "
                               "and represents the rows of the 2D array. The x-indexing is counted from left to right "
                               "and represents the columns of the 2D array.",
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    }
                }
            },
            "start_times": {
                "description": "The array that contains that start time values for each x,y slice."
                               "As date-time string format ISO 8601 must be supported, or a program language specific "
                               "data-type that represents date and time.",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "end_times": {
                "description": "The vector that contains that end time values for each x,y slice, in case the "
                               "the time stamps for all or a subset of slices are intervals. For time instances "
                               "the from and to time stamps must be equal or empty. "
                               "As date-time string format ISO 8601 must "
                               "be supported, or a program language specific data-type that represents date and time.",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "extent": {
                "description": "The spatial extent of the data set.",
                "type": "object",
                "properties": {
                    "north": {
                        "description": "The northern border.",
                        "type": "number"
                    },
                    "south": {
                        "description": "The southern border.",
                        "type": "number"
                    },
                    "east": {
                        "description": "The eastern border.",
                        "type": "number"
                    },
                    "west": {
                        "description": "The western border.",
                        "type": "number"
                    },
                    "nsres": {
                        "description": "The north-south resolution in projection units.",
                        "type": "number"
                    },
                    "ewres": {
                        "description": "The east-west resolution in projection units.",
                        "type": "number"
                    },
                },
                "example": {
                    "id": "test_data",
                    "start_times": ("2001-01-01T00:00:00",
                                    "2001-01-02T00:00:00",
                                    "2001-01-03T00:00:00"),
                    "end_times": ("2001-01-02T00:00:00",
                                  "2001-01-03T00:00:00",
                                  "2001-01-04T00:00:00"),
                    "data": (
                        (
                            (0, 0, 0),
                            (1, 1, 1),
                            (2, 2, 2)
                        ),
                        (
                            (0, 0, 0),
                            (1, 1, 1),
                            (2, 2, 2)
                        ),
                        (
                            (0, 0, 0),
                            (1, 1, 1),
                            (2, 2, 2)
                        )
                    )
                }
            }
        }
    }
}
