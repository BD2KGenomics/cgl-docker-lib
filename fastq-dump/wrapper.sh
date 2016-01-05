#!/usr/bin/env bash

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    UID=$(stat -c '%u:%g' /data)
    chown -R $UID /data
}
trap finish EXIT

# Call tool with parameters
./../opt/fastq-dump/sratoolkit.2.5.7-ubuntu64/bin/vdb-config --import /data/*.ngc /data && \
./../opt/fastq-dump/sratoolkit.2.5.7-ubuntu64/bin/fastq-dump "$@"
