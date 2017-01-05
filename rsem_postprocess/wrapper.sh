#!/usr/bin/env bash
# Call tool with parameters
sh /opt/cgl-docker-lib/rsem_postprocess.sh "$*"
# Fix ownership of output files
UID=$(stat -c '%u' /data)
chown -R $UID /data
