#!/bin/bash

export PORT=5000
export START_NGINX=1

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

# Start the nginx process by request
if [ "${START_NGINX}" -eq 1 ]; then
    # Run the nginx server
    nginx -g "daemon off;"
fi
