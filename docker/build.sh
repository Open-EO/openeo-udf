#!/bin/bash
# Build it
#docker build -t openeo_udf .
# Test it
#docker run_json_user_code -p 5100:5100 -p 5200:5200 -it openeo_udf


JSON='
{
  "code": {
    "code": "print(data)\ndata.get_raster_collection_tiles()\ndata.del_feature_collection_tiles()\n",
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
    ],
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
'

curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://localhost:5100/udf
