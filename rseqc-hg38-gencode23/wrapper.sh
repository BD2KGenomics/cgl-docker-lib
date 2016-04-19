#!/usr/bin/env bash
set -e

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    user_id=$(stat -c '%u:%g' /data)
    chown -R ${user_id} /data
}
trap finish EXIT

display_usage() {
	echo "This script requires 2 arguments: path to BAM and UUID"
	echo -e "\nUsage:\ndocker run -v <src:dst> quay.io/ucsc_cgl/rseqc-hg38-gencode23 /dst/BAM UUID \n"
	}

# if less than three arguments supplied, display usage
if [  $# -le 1 ]
	then
		display_usage
		exit 1
	fi

# Call tool with parameters
/opt/RSeQC-2.6.3/rseqc.sh "$@"
