#!/usr/bin/env bash
# Call tool with parameters
samtools "$@"
# Fix ownership of output files
UID=$(stat -c '%u:%g' /data)
chown -R $UID /data