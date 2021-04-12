====================
OpenEO UDF Framework
====================

OpenEO User Defined Functions (UDF) are an approach to run arbitrary code on geographical data
that is available in an OpenEO processing backend like R, GRASS GIS or GeoTrellis.
This document describes the UDF interface and provides reference implementation for Python3. The reference
implementation includes:

    - An OpenEO UDF REST test server that processes user defined data with user defined functions
      and describes its interface using OpenAPI 3.0.
    - A Python3 API that specifies how UDF must be implemented in Python3

Documentation is available online (see list below) and through the test server.

    - UDF Framework: https://open-eo.github.io/openeo-udf/
    - API description: https://open-eo.github.io/openeo-udf/api_docs/

Backend integration
===================

This UDF implementation contains an abstract OpenAPI 3.0 description of schemas that must be used when an API for a specific
programming language is implemented.
The schemas are generated from the UDF python3 classes of the REST service, that are implemented using pydantic.
The documentation will be generated on the fly and can be accessed via browser from the docker container or when the
udf server started from localhost.

The following files implement the schemas:

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/legacy/dimension_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/legacy/feature_collection_legacy_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/datacube_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/machine_learn_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/legacy/datacube_legacy_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/bounding_box_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/structured_data_schema.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/server/data_model/udf_schemas.py

The basis of the OpenAPI 3.0 description are basic data-types that are available in many programming languages.
These basic data-types are:

    - Strings
    - Floating point values
    - Integer values
    - Date and time data-types
    - Multi-dimensional arrays, lists or vectors of floating point values, integer values and date time data-types
    - Maps or dictionaries

The entry point of an UDF is a single dictionary or map, that can be represented by a class object as well,
depending on the programming language.

The schemas SpatialExtentSchema, FeatureCollectionTileSchema, HyperCubeSchema,
StructuredDataSchema, MachineLearnModelSchema and UdfDataSchema are a OpenAPI 3.0 based definitions for the UDF API.
These schemas are implemented as python3 classes with additional functionality in the Python3 REST test server.

The schemas UdfCodeSchema, UdfRequestSchema and ErrorResponseSchema are used by the UDF
test server to provide the POST endpoint. They are not part of the UDF API.

To support UDF's in the backend the following approaches can be used:

  - The backend implements for specific languages the UDF API based on the provided OpenAPI 3.0 description
  - The backend uses the Python prototype implementation for Python based UDF's
  - The backend uses the UDF test server to run Python UDF's with JSON protocol or message pack binary protocol

Installation
============

The installation was tested on ubuntu 16.04 and 18.04. It requires python3.6  and pip3. It will install
several python3 libraries like pygdal [#pygdal]_, pytorch [#pytorch]_, scikit-learn [#scikit]_,
tensorflow [#tensorflow]_ and other libraries that require additional development files on the host system.
The python3 message pack library [#messagepack]_ is used for binary serialization support in the REST interface

.. rubric:: Footnotes

.. [#pygdal] https://github.com/nextgis/pygdal
.. [#pytorch] https://pytorch.org/
.. [#scikit] http://scikit-learn.org/stable/
.. [#tensorflow] https://www.tensorflow.org/
.. [#messagepack] https://msgpack.org/


Local installation
------------------

1. Clone the git repository into a specific directory and create the virtual python3 environment:

    .. code-block:: bash

        mkdir -p ${HOME}/src/openeo
        cd ${HOME}/src/openeo

        git clone https://github.com/Open-EO/openeo-udf.git

        virtualenv -p python3 venv
    ..

2. Install are requirements in the virtual environment:

    .. code-block:: bash

        source venv/bin/activate
        cd openeo-udf
        pip3 install -r requirements.txt
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
        firefox _build/html/index.html &
        cd ..
    ..

4. Run the udf server and have a look at the OpenAPI documentation. Here you can also
    download the swagger definition:

    .. code-block:: bash

        run_udf_server &

        firefox http://localhost:5000/redoc
        firefox http://localhost:5000/docs
    ..

Docker image
------------

The openeo-udf repository contains the build instruction of an openeo-udf docker image.


1. Clone the git repository into a specific directory and create the virtual python3 environment:

    .. code-block:: bash

        mkdir -p ${HOME}/src/openeo
        cd ${HOME}/src/openeo

        git clone https://github.com/Open-EO/openeo-udf.git

    ..

2. Build the docker image and run it:

    .. code-block:: bash

        cd openeo-udf/docker
        docker build -t openeo_udf .
        docker run --name "openeo-udf-server" -p 5000:5000 -p 80:80 -t openeo_udf
    ..

3. Have a look at the documentation that is available in the docker deployment. This includes
   this document with the python3 API description, that must be used in the UDF's and the swagger
   documentation of the REST UDF service:

    .. code-block:: bash

        # This document
        firefox http://localhost/index.html

        # The python3 API description that must be used in the python3 UDF
        firefox http://localhost/index.html

        # The swagger API description
        firefox http://localhost:5000/redoc
        firefox http://localhost:5000/docs

        # Download the swagger JSON file
        wget http://localhost:5000/api/v0/swagger.json
    ..


Using the API to code an UDF
============================

The python3 reference implementation provides an API to implement UDF conveniently. It makes use
of many python3 libraries that provide functionality to access raster and vector geo-data.

The following libraries should be used implementations UDF's:

    * The python3 library numpy [#numpy]_ should be used to process the raster data.
    * The python3 library geopandas [#geopandas]_ and shapely [#shapely]_ should be used to process the vector data.
    * The python3 library pandas [#pandas]_, specifically pandas.DatetimeIndex should be used to process time-series data
    * The python3 library xarray [#xarray]_ for hypercube computations
    * The python3 libraries pytorch [#pytorch]_ and scikit-learn [#scikit]_ for machine model support

.. rubric:: Footnotes

.. [#numpy] http://www.numpy.org/
.. [#geopandas] http://geopandas.org/index.html
.. [#shapely] https://github.com/Toblerity/Shapely
.. [#pandas] http://pandas.pydata.org/
.. [#xarray] https://xarray.pydata.org/en/stable/


The python3 API is well documented and fully tested using doctests. The doctests show
the handling of the API with simple examples. This document and the full API description
is available when you installed openeo_udf locally or if you use the docker image.
However, the original python3 file that implements the OpenEO UDF python3 API is available here:

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/collection_base.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/feature_collection.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/datacube.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/machine_learn_model.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/spatial_extent.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/structured_data.py
    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/api/udf_data.py

The UDF's are directly available for download from the repository:


    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_ndvi.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_pytorch_ml.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_statistics.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_sklearn_ml.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_map_fabs.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_reduce_time_mean.py

    * https://github.com/Open-EO/openeo-udf/blob/master/src/openeo_udf/functions/datacube_reduce_time_sum.py

Several UDF were implemented and provide and example howto develop an UDF. Unittest were implemented for
each UDF including machine learn models and hypercube approach. The tests are available here:

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_map_fabs.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_ndvi.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_pytorch_ml.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_mean.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_sum.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_sklearn_ml.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_udf_hypercube_pytorch_ml.py

    * https://github.com/Open-EO/openeo-udf/blob/master/tests/test_ml_storage.py

The following classes are part of the UDF Python API and should be used for implementation of UDF's and backend Python
driver:

    * SpatialExtent
    * Hypercube
    * FeatureCollection
    * StructuredData
    * MachineLearnModel
    * UdfData

**The implementation of an UDF should be performed by cloning the openEO UDF repository and install
it locally or in a docker container.** The UDF repository is designed to support the implementation
of python3 UDF's without running it in a dedicated backend.

    1. Look at the existing and well documented UDF functions
    2. Implement your own function and put it into the **functions** directory for easier access in your tests
    3. Clone an existing unittest in the test directory and write your tests with generic raster, vector or xarray data


Using the UDF server
--------------------

**Vector Example**

The second examples applies a buffer operation on a feature collection. It computes a buffer of size 5
on all features of the first feature collection tile and stores the result in the input **data**
object:

    .. code-block:: python

        tile = data.get_feature_collection_tiles()[0]
        buf = tile.data.buffer(5)
        new_data = tile.data.set_geometry(buf)
        data.set_feature_collection_tiles([FeatureCollectionTile(id=tile.id + "_buffer", data=new_data, start_times=tile.start_times, end_times=tile.end_times),])
    ..


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
      }

   ..
