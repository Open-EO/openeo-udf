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
