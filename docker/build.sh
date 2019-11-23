#!/bin/bash
# Build it
# docker build --no-cache -t openeo_udf .
docker build -t openeo_udf .

# Test it with enabled nginx
mkdir /tmp/www
docker run -v /tmp/www:/var/www/http --name "openeo-udf-server" -p 5000:5000 -p 8080:80 -t -e START_NGINX=1 openeo_udf

docker stop "openeo-udf-server" &&  docker rm "openeo-udf-server"

# Documentation
curl -X GET http://localhost:8080/index.html
curl -X GET http://localhost:8080/api_docs/index.html
curl -X GET http://localhost:5000/redoc
curl -X GET http://localhost:5000/docs
wget http://localhost:5000/openapi.json -O /tmp/openeo_udf.json


JSON='
{
  "code": {
    "source": "tile = data.get_feature_collection_tiles()[0] \nbuf = tile.data.buffer(5) \nnew_data = tile.data.set_geometry(buf) \ndata.set_feature_collection_tiles([FeatureCollectionTile(id=tile.id + \"_buffer\", data=new_data, start_times=tile.start_times, end_times=tile.end_times),])\n",
    "language": "python"
  },
  "data": {
    "proj": {"EPSG":4326},
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

curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://localhost:5000/udf

