# Computational Genomics Lab, Genomics Institute, UC Santa Cruz
### Running the ADAM preprocessing pipeline container

This guide will walk through running the ADAM preprocessing pipeline. If you
find any errors or corrections please feel free to make a pull request against
the [cgl-docker-lib](https://github.com/BD2KGenomics/cgl-docker-lib) repository,
where this Docker image is maintained. Feedback of any kind is appreciated.

## Overview

This container runs the [ADAM preprocessing
pipeline](https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/adam_pipeline),
which is built using [Toil](https://github.com/BD2KGenomics/toil), a
high-performance workflow execution system. [ADAM](https://github.com/bigdatagenomics/adam)
is a parallel system for processing genomic data that is built on top of [Apache
Spark](https://spark.apache.org). Although ADAM and Apache Spark are designed
to be run as a distributed system, this container is designed to run on a
single node. If you would like to run ADAM on a Spark cluster, look at the [ADAM
preprocessing workflow in
toil-scripts](https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/adam_pipeline).

This pipeline expects one input, which is aligned reads in SAM/BAM/ADAM format.
Additionally, we expect a path to a known sites file. This is a file that
describes positions where variants are known to occur, and is used to mask
out sites during base quality score recalibration. Typically, a dbSNP VCF file
is used. This pipeline requires a run environment with at least 10G of memory
to run BQSR with a known sites file from dbSNP. You should provide a path where
the output data should be written.

## Testing

There is an automated test included simply install Docker, make, and Python 2.7 for your
platform and do the following:

    make test

This will run a very small test SAM file.

## Running

```
docker run \
    -v /foo/bar:/foo/bar \
    quay.io/ucsc_cgl/adam-pipeline \
    --sample /foo/bar/<input_sample>.{sam,bam} \
    --known-sites /foo/bar/<known_sites>.vcf \
    --output /foo/bar/<path_to_write_output> \
    --memory <memory_setting>
```

The memory setting for this pipeline is used to set the amount of memory used
by ADAM, and should be the amount of memory in gigabytes that you would like
to allocate.

## Running in Cromwell

Before you attempt this make sure you have Cromwell installed and have built the
container above using `make test` (or the container has been pushed to quay.io).

Then make sure you update workflow.json so the paths are correct for your system.

You can run this tool with a very simple WDL workflow using the following:

    cromwell run workflow.wdl workflow.json

Look for the output bam where you specified in the `workflow.json`.
