#!/usr/bin/env bash

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    UID=$(stat -c '%u:%g' /data)
    chown -R $UID /data
}
trap finish EXIT

# Call tool with parameters
python /opt/mapsplice/MapSplice_multi_threads_2.0.1.9/mapsplice.py "$@"
