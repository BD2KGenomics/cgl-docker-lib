#!/usr/bin/env bash
# Call tool with parameters
picard-tools "$@"
# Fix ownership of output files
UID=$(stat -c '%u:%g' /data)
chown -R $UID /data