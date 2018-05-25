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

The argument of an UDF is a single dictionary or map, that can be represented by a class object as well,
depending on the programming language.


Installation
============

The installation was tested on ubuntu 16.04 and 18.04. It requires python3.6  and pip3. It will install
several python3 libraries like pygdal [#pygdal]_, pytorch [#pytorch]_, scikit-learn [#scikit]_,
tensorflow [#tensorflow]_ and other libraries that require additional development files on the host system.


.. rubric:: Footnotes

.. [#pygdal] https://github.com/nextgis/pygdal
.. [#pytorch] https://pytorch.org/
.. [#scikit] http://scikit-learn.org/stable/
.. [#tensorflow] https://www.tensorflow.org/


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

        python3 setup.py install
        python3 setup.py test
        python3 tests/test_doctests.py
    ..

3. Create the UDF documentation that includes the python3 API description and start firefox to read it:

    .. code-block:: bash

        cd docs
        make html
        firefox _build/html/index.html
    ..

4. Run the udf server:

    .. code-block:: bash

        run_udf_server
    ..

5. Run the UDF execution command line tool:

    .. code-block:: bash

        execute_udf data/red_nir_1987.tif,data/red_nir_2000.tif,data/red_nir_2002.tif RED,NIR\
                    /tmp src/openeo_udf/functions/raster_collections_ndvi.py

        execute_udf data/red_nir_1987.tif,data/red_nir_2000.tif,data/red_nir_2002.tif RED,NIR\
                    /tmp src/openeo_udf/functions/raster_collections_reduce_time_sum.py

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
        docker run --name "openeo-udf-server" -p 5000:5000 -p 80:80 -t openeo_udf
    ..

3. have a look at the documentation that is available in the docker deployment. This includes
   this document with the python3 API description, that must be used in the UDF's and the swagger
   documentation of the REST UDF service:

    .. code-block:: bash

        # This document
        firefox http://localhost/index.html
        # The python3 API description that must be used in the python3 UDF
        firefox http://localhost/api/openeo_udf.api.html#module-openeo_udf.api.base
        # The swagger API description
        firefox http://localhost/api_docs/index.html
    ..


Coding an UDF
=============

The python3 reference implementation provides an API to implement UDF conveniently. It makes use
of many python3 libraries that provide functionality to access raster and vector geo-data.

The following libraries should be used implementations UDF's:

    * The python3 library numpy [#numpy]_ should be used to process the raster data.
    * The python3 library geopandas [#geopandas]_ and shapely [#shapely]_ should be used to process the vector data.
    * The python3 library pandas [#pandas]_, specifically pandas.DatetimeIndex should be used to process time-series data

.. rubric:: Footnotes

.. [#numpy] http://www.numpy.org/
.. [#geopandas] http://geopandas.org/index.html
.. [#shapely] https://github.com/Toblerity/Shapely
.. [#pandas] http://pandas.pydata.org/

The python3 API is well documented and fully tested using doctests. The doctests show
the handling of the API with simple examples. This document and the full API description
is available when you installed openeo_udf locally or if you use the docker image.
However, the original python3 file that implements the OpenEO UDF python3 API is available here:

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/base.py

Several UDF were implemented and provide and example howto develop an UDF. The UDF's are directly available for
download from the repository:

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/raster_collections_ndvi.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/raster_collections_reduce_time_min_max_mean_sum.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/raster_collections_reduce_time_sum.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/feature_collections_buffer.py

Using the UDF command line tool
-------------------------------

The python3 reference implementation provides a command line tool to run a UDF on raster images that
are supported by GDAL. At the moment only GeoTiff files are tested. The command line tool
allows to run any UDF on a list or multi-band GeoTiff files. The command line tool has a simple
help interface:

    .. code-block:: bash

        (openeo_venv) user@t61:~/src/openeo/openeo-udf$ execute_udf --help
        usage: execute_udf [-h] raster_files band_names raster_output_dir path_to_udf

        This program reads a list of single- or multi-band GeoTiff files and applies a user defined function (UDF)
        on them. The GeoTiff files must be provided as comma separated list, as well as the band names. The UDF
        must be accessible on the file system. The computed results are single- or multi-band GeoTiff files
        that are written into a specific output directory.

        Examples:

            The following command computes the NDVI on a raster
            image series of three multi-band tiff files. Two bands are provided with the names RED and NIR for
            the UDF. The three resulting single-band GeoTiff files are written to the /tmp directory.

                execute_udf data/red_nir_1987.tif,data/red_nir_2000.tif,data/red_nir_2002.tif RED,NIR \
                            /tmp src/openeo_udf/functions/raster_collections_ndvi.py

            The next command computes the sum of the raster series for each band. A single raster image
            with two bands is written as GeoTiff file to the directory /tmp.

                execute_udf data/red_nir_1987.tif,data/red_nir_2000.tif,data/red_nir_2002.tif RED,NIR\
                            /tmp src/openeo_udf/functions/raster_collections_reduce_time_sum.py

        positional arguments:
          raster_files       Comma separated list of raster files. If several raster
                             files are provided, then each raster file must have the
                             same number of bands.
          band_names         A comma separated list of band names.
          raster_output_dir  The output directory to store the computed results.
          path_to_udf        The UDF file to execute.

        optional arguments:
          -h, --help         show this help message and exit

    ..


Using the UDF server
--------------------

**Raster Example**

In the first example the raster collection tiles are removed from the provided data.

The following JSON definition includes the python3 code
and a simple raster collection with two 2x2 tiles with two start and end time stamps.

    .. code-block:: json

      {
        "code": {
          "source": "data.del_raster_collection_tiles()",
          "language": "python"
        },
        "data": {
          "proj": "EPSG:4326",
          "raster_collection_tiles": [
            {
              "data": [
                [
                  [
                    0,
                    1
                  ],
                  [
                    2,
                    3
                  ]
                ],
                [
                  [
                    0,
                    1
                  ],
                  [
                    2,
                    3
                  ]
                ]
              ],
              "extent": {
                "north": 53,
                "south": 50,
                "east": 30,
                "nsres": 0.01,
                "ewres": 0.01,
                "west": 24
              },
              "end_times": [
                "2001-01-02T00:00:00",
                "2001-01-03T00:00:00"
              ],
              "start_times": [
                "2001-01-01T00:00:00",
                "2001-01-02T00:00:00"
              ],
              "id": "test_data",
              "wavelength": 420
            }
          ]
        }
      }

    ..

Running the code, with the assumption that the JSON code was
placed in the shell environmental variable "JSON", should look like this:

    .. code-block:: bash

        curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://localhost:5000/udf
    ..

The result of the processing should be the elimination of the raster and feature collections,
since the provided data object will be used to create the resulting data:

    .. code-block:: json

        {
          "feature_collection_tiles": [],
          "models": {},
          "proj": "EPSG:4326",
          "raster_collection_tiles": []
        }
    ..

Hence, a data object that contains the raster and feature collections is provided to the
user defined function. The UDF code works on the data and stores the result in the same data object.

**Vector Example**

The second examples applies a buffer operation on a feature collection.

The following JSON definition includes the python3 code that applies the buffer operation and
a simple feature collection that contains two points with start and end time stamps.

    .. code-block:: json

      {
        "code": {
          "source": "tile = data.get_feature_collection_tiles()[0] \nbuf = tile.data.buffer(5) \nnew_data = tile.data.set_geometry(buf) \ndata.set_feature_collection_tiles([FeatureCollectionTile(id=tile.id + \"_buffer\", data=new_data, start_times=tile.start_times, end_times=tile.end_times),])\n",
          "language": "python"
        },
        "data": {
          "proj": "EPSG:4326",
          "feature_collection_tiles": [
            {
              "id": "test_data",
              "data": {
                "features": [
                  {
                    "geometry": {
                      "coordinates": [
                        24,
                        50
                      ],
                      "type": "Point"
                    },
                    "id": "0",
                    "type": "Feature",
                    "properties": {
                      "a": 1,
                      "b": "a"
                    }
                  },
                  {
                    "geometry": {
                      "coordinates": [
                        30,
                        53
                      ],
                      "type": "Point"
                    },
                    "id": "1",
                    "type": "Feature",
                    "properties": {
                      "a": 2,
                      "b": "b"
                    }
                  }
                ],
                "type": "FeatureCollection"
              },
              "end_times": [
                "2001-01-02T00:00:00",
                "2001-01-03T00:00:00"
              ],
              "start_times": [
                "2001-01-01T00:00:00",
                "2001-01-02T00:00:00"
              ]
            }
          ]
        }
      }

    ..


Running the code, with the assumption that the JSON code was
placed in the shell environmental variable "JSON", should look like this:

    .. code-block:: bash

        curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://localhost:5000/udf
    ..

The result of the processing are two polygons (coordinates are truncated):

    .. code-block:: json

      {
        "feature_collection_tiles": [
          {
            "data": {
              "features": [
                {
                  "geometry": {
                    "coordinates": [
                      [
                        [
                          29.0,
                          50.0
                        ],
                        [
                          "..."
                        ],
                        [
                          29.0,
                          50.0
                        ]
                      ]
                    ],
                    "type": "Polygon"
                  },
                  "id": "0",
                  "properties": {
                    "a": 1,
                    "b": "a"
                  },
                  "type": "Feature"
                },
                {
                  "geometry": {
                    "coordinates": [
                      [
                        [
                          35.0,
                          53.0
                        ],
                        [
                          "..."
                        ],
                        [
                          35.0,
                          53.0
                        ]
                      ]
                    ],
                    "type": "Polygon"
                  },
                  "id": "1",
                  "properties": {
                    "a": 2,
                    "b": "b"
                  },
                  "type": "Feature"
                }
              ],
              "type": "FeatureCollection"
            },
            "end_times": [
              "2001-01-02T00:00:00",
              "2001-01-03T00:00:00"
            ],
            "id": "test_data_buffer",
            "start_times": [
              "2001-01-01T00:00:00",
              "2001-01-02T00:00:00"
            ]
          }
        ],
        "models": {},
        "proj": "EPSG:4326",
        "raster_collection_tiles": []
      }

   ..

