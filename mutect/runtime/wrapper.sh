#!/usr/bin/env bash
# Call tool with parameters
java $JAVA_OPTS /opt/mutect/mutect-1.1.7.jar "$@"
# Fix ownership of output files
UID=$(stat -c '%u' /data)
GID=$(stat -c '%g' /data)
chown -R $UID:$GID /data