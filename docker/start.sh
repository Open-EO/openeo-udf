#!/bin/bash

export PORT=5000

# Update the udf repository and create the documentation for the nginx server
cd /tmp/src/openeo_udf/
git pull origin master
python3 setup.py install
cd docs
make html

# Copy the docs into the default www dir
cp -r _build/html/* /var/www/html/.

# Run the udf server
run_udf_server --port ${PORT} --host 0.0.0.0 &
# Wait for the server to start
sleep 3

# Catch the swagger json description
wget http://localhost:5000/api/v0/swagger.json -O /tmp/openeo_udf.json

# Then run spectacle to generate the HTML documentation
spectacle /tmp/openeo_udf.json -t /var/www/html/api_docs

# Run the nginx server
nginx -g "daemon off;"
