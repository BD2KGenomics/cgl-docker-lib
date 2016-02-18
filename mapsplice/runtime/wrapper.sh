#!/usr/bin/env bash

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    user_id=$(stat -c '%u:%g' /data)
    chown -R ${user_id} /data
}
trap finish EXIT

# Call tool with parameters
python /opt/mapsplice/MapSplice-v2.1.8/mapsplice.py "$@"
