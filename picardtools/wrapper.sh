#!/usr/bin/env bash

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    UID=$(stat -c '%u:%g' /data)
    chown -R $UID /data
}
trap finish EXIT

# Call tool with parameters
picard-tools "$@"
