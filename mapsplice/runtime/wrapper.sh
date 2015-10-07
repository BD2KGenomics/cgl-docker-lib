#!/usr/bin/env bash
# Call tool with parameters
python /opt/mapsplice/MapSplice-v2.1.8/mapsplice.py "$@"
# Fix ownership of output files
UID=$(stat -c '%u' /data)
GID=$(stat -c '%g' /data)
chown -R $UID:$GID /data