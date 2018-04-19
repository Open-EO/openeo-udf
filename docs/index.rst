====================
OpenEO UDF Framework
====================

This is the description of the OpenEO User Defined Function (UDF) API that must be applied when implementing
UDF for the OpenEO backends.

This document describes the UDF interface and provides reference implementation for Python.

Basic datatypes
===============

The basis of the interface description are basic data-types that are available in many programming languages.
These basic data-types are:

   - Strings
   - Floating point values
   - Integer values
   - Date and time data-types
   - Multi-dimensional arrays, lists or vectors of floating point values, integer values and date time data-types
   - Maps or dictionaries

The argument of a UDF is a single dictionary or map, that can be represented by a class object as well,
depending on the programming language.

The return value is a dictionary as well.

Swagger description
===================

The data chunk that represent a subset of data from a spatio-temporal dataset:

   .. code-block:: python

      "data_chunk": {
         "description": "A chunk of data that represents a spatio-temporal subset of a spatio-time dataset. "
                        "The apporach to implement these datatypes can be different between the programming "
                        "languages. For Python we suggest to use **pandas.DatetimeIndex** for the one dimensional "
                        "time arrays and **numpy.ndarray**'s for the data."
         "type": "object",
         "required": [
            "data",
            "from"
         ],
         "data": {
            "description": "A three dimensional array fo integer (8,16,32,64 bit) or float (16, 32, 64 bit) values."
                           "The index dimension is as follows: [time][y][x]. Hence, the index data[0] returns "
                           "the 2D slice for the first time-stamp. The y-indexing if counted from top to bottom "
                           "and represents the rows of the 2D array. The x-indexing is counted from left to right "
                           "and represents the columns of the 2D array.",
            "type": "array",
            "items": {
               "type": "array"
                  "items": {
                     "type": "array"
                        "items": {
                           "type": "number"
                           }
                     }
               }
            }
         },
         "from": {
            "description": "The vector that contains that start time values for each x,y slice."
                           "As date-time string format ISO 8601 must be supported, or a program language specific "
                           "data-type that represents date and time.",
            "type": "array",
            "items": {
               "type": "string"
               }
            }
         },
         "to": {
            "description": "The vector that contains that end time values for each x,y slice, in case the "
                           "the time stamps for all or a subset of slices are intervals. For time instances "
                           "the from and to time stamps must be equal. As date-time string format ISO 8601 must "
                           "be supported, or a program language specific data-type that represents date and time.",
            "type": "array",
            "items": {
               "type": "string"
               }
            }
         },
         "id": {
            "description": "The identifier of this data chunk.",
            "type": "string"
            }
         },
         "example": {
            "id": "test_data",
            "from": ("2001-01-01T00:00:00",
                     "2001-01-02T00:00:00",
                     "2001-01-03T00:00:00"),
            "to": ("2001-01-02T00:00:00",
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
                        (,
                        )
                            (0, 0, 0),
                            (1, 1, 1),
                            (2, 2, 2)
                        )
                    )
         }
      }

   ..


Contents
========

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
