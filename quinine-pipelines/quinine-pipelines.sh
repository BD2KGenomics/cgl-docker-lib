#!/bin/bash

set -e

# make a temp dir for the jobstore
jobStoreDir=$(mktemp -d -t jobStoreXXXXX)

# run
export PYTHONPATH=/opt/toil-scripts/src/
python -m toil_scripts.quinine_pipelines.metrics $@ \
    --defaultDisk 0 \
    --maxDisk 0 \
    ${jobStoreDir}/jobStore

# remove the jobstore
rm -rf jobStoreDir
