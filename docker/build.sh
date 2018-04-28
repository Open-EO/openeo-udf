#!/bin/bash
# Build it
docker build -t openeo_udf .
# Test it
docker run -t openeo_udf
