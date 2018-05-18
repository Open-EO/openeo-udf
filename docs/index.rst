====================
OpenEO UDF Framework
====================

This is the description of the OpenEO User Defined Function (UDF) API that must be applied when implementing
UDF for the OpenEO backends.

This document describes the UDF interface and provides reference implementation for Python. The reference
implementation includes an UDF REST server, that processes user defined data with user defined functions
and describes its interface using swagger2.0.

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


Installation
============

The installation was tested on ubuntu 16.04 and 18.04. It requires python3.6  and pip3. It will install numpy,
rasterio, pytorch, scikit, tensorflow and other libraries that require additional development files on the host system.


Local installation
------------------

1. Clone the git repository into a specific directory and create the virtual python3 environment:

    .. code-block:: bash

        mkdir -p ${HOME}/src/openeo
        cd ${HOME}/src/openeo

        git clone https://github.com/Open-EO/openeo-udf.gi
        virtualenv -p python3 openeo_venv
    ..

2. Install are requirements in the virtual environment:

    .. code-block:: bash

        source openeo_venv/bin/activate
        cd openeo-udf
        pip3 install -r requirements.txt
        pip3 install rasterio
    ..


3. Install the openeo-udf software and run the tests:

    .. code-block:: bash

        make install
        make test

    ..

3. Create the UDF documentation that includes the python3 API description:

    .. code-block:: bash

        cd html
        make html

    ..

4. Run the udf server:

    .. code-block:: bash

        run_udf_server
    ..

Docker image
------------

The openeo-udf repository contains the build instruction of an openeo-udf docker image:


1. Clone the git repository into a specific directory and create the virtual python3 environment:

    .. code-block:: bash

        mkdir -p ${HOME}/src/openeo
        cd ${HOME}/src/openeo

        git clone https://github.com/Open-EO/openeo-udf.gi
    ..

2. Build the docker image and run it:

    .. code-block:: bash

        cd openeo-udf/docker
        docker build -t openeo_udf .

    ..

Implementing an UDF
===================

The python3 reference implementation provides an API to implement UDF conveniently. It makes use
of many python3 libraries that provide functionalities to access raster and vector geodata.
Several UDF were implemented and provide and example howto develop an UDF.

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
