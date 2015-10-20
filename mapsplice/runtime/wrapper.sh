#!/usr/bin/env bash
# Call tool with parameters
python /opt/mapsplice/MapSplice-v2.1.8/mapsplice.py "$@"
# Fix ownership of output files
UID=$(stat -c '%u:%g' /data)
chown -R $UID /data