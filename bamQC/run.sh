#!/bin/bash
UUID=$(cat /proc/sys/kernel/random/uuid)

#!/usr/bin/env bash
set -e

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    user_id=$(stat -c '%u:%g' /data)
    chown -R ${user_id} /data
}
trap finish EXIT

echo "Sorting by name..."
sambamba sort -t 4 --sort-by-name --out /data/$UUID.sortedByName.bam $1

echo "Marking duplicates..."
sambamba view -h /data/$UUID.sortedByName.bam | samblaster \
  | sambamba view --sam-input --format bam /dev/stdin > /data/$UUID.sortedByName.md.bam
rm /data/$UUID.sortedByName.bam

echo "Sorting by coordinate..."
sambamba sort --show-progress -t 4 --out=/data/$UUID.sortedByCoord.md.bam /data/$UUID.sortedByName.md.bam
rm /data/$UUID.sortedByName.md.bam

echo "Counting reads..."
read_distribution.py -i /data/$UUID.sortedByCoord.md.bam -r /ref/hg38_GENCODE_v23_basic.bed  > $2/readDist.txt
Rscript --vanilla /app/parseReadDist.R $2/readDist.txt
mv /data/$UUID.sortedByCoord.md.bam $2/sortedByCoord.md.bam
mv /data/$UUID.sortedByCoord.md.bam.bai $2/sortedByCoord.md.bam.bai