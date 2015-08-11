#!/usr/bin/env bash
# Call tool with parameters
python /opt/cgl-docker-lib/MapSplice-v2.1.8/mapsplice.py "$@"
# Fix ownership of output files
UID=$(stat -c '%u' /data)
chown -R $UID /data
