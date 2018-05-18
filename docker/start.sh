#!/bin/bash

export PORT=5100
export DOC_PORT=5200

run_udf_server --port ${PORT} --host 0.0.0.0 &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start udf server: $status"
  exit $status
fi

sleep 3

cd /tmp/src
wget http://localhost:${PORT}/api/v0/swagger.json
spectacle -d --port ${DOC_PORT} swagger.json
