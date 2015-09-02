#!/usr/bin/env bash
# Call tool with parameters
java $JAVA_OPTS -jar /opt/cgl-docker-lib/gatk.jar "$@"
# Fix ownership of output files
UID=$(stat -c '%u' /data)
chown -R $UID /data
