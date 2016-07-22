# Computational Genomics Lab, Genomics Institute, UC Santa Cruz
### Running the Quinine pipeline container

This guide will walk through running the Quinine pipeline. If you
find any errors or corrections please feel free to make a pull request against
the [cgl-docker-lib](https://github.com/BD2KGenomics/cgl-docker-lib) repository,
where this Docker image is maintained. Feedback of any kind is appreciated.

## Overview

This container runs the [Quinine](https://github.com/bigdatagenomics/quinine) QC
tool. This tool builds on top of the
[ADAM](https://github.com/bigdatagenomics/adam) platform for processing genomic
data using [Apache Spark](https://spark.apache.org) and the [Toil](
https://github.com/BD2KGenomics/toil) workflow management system.

This container runs three separate workflows:

1. RNA-seq QC: Computes a set of quality control metrics for RNA-seq data.
2. Targeted QC: Computes a set of quality control metrics for targeted
   sequencing data captured using hybrid selection bait.
3. Contamination estimation: Estimates the inter-sample contamination using VCF
   files to compute the background allele frequency, and by then looking at read
   data from homozygous alt sites in a sample.

## Testing

There is an automated test included simply install Docker, make, and Python 2.7 for your
platform and do the following:

```
make test
```

This test runs on a small set of test inputs, and tests all three workflows.

## Running

See `test.py` for example tool invocations. Additionally, we have provided WDL
workflows for each of the three stages. These workflows run by default on the
test files in the `test/` directory. If `cromwell` is on your path, or
`${CROMWELL_HOME}` is set, these WDL files will be run as part of `make test`.
