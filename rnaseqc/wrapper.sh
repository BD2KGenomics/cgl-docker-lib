#!/usr/bin/env bash

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    user_id=$(stat -c '%u:%g' /data)
    chown -R ${user_id} /data
}
trap finish EXIT

# Call tool with parameters
java $JAVA_OPTS -jar /opt/rnaseqc/RNA-SeQC_v1.1.8.jar "$@"

