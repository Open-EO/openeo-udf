#!/bin/bash
# Build it
docker build -t openeo_udf .
# Test it
docker run -p 5100:5100 -p 5200:5200 -it openeo_udf
