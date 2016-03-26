#!/usr/bin/env bash
set -e

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    user_id=$(stat -c '%u:%g' /data)
    chown -R ${user_id} /data
}
trap finish EXIT

# Copy credentials
cp /data/*boto ~/.boto
# Call tool with parameters
python /opt/s3-multipart/s3-mp-download.py "$@"
