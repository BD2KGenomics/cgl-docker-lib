# Computational Genomics Lab, Genomics Institute, UC Santa Cruz
### Running the CGL Exome Pipeline Container: Release 2.0.8

This guide will walk through running the pipeline from start to finish. If there are any questions please contact
John Vivian (jtvivian@gmail.com). If you find any errors or corrections please feel free to make a pull request.
Feedback of any kind is appreciated.

## Overview

This container runs the 
[CGL Exome pipeline](https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/exome_variant_pipeline), which
is built using [Toil](https://github.com/BD2KGenomics/toil), a high-performance pipeline architecture platform for
running workflows. This container is designed to run local samples. This pipeline expects one sample to be in the form of a normal BAM file and a tumor BAM file. 
A sample, which consists of a tumor and normal BAM file, can be passed via the command line options `--normal`, `--tumor`, and `--uuid`. If wanting to run more than one sample, then the use the `toil-exome --generate-manifest` command and fill in the manifest as instructed. All samples and inputs must be submitted as URLs with support for the following schemas: `http://`, `file://`, `s3://`, `ftp://`.

This pipeline needs approximately 15G of RAM in order to run various GATK steps.

This pipeline **requires** a host with Docker installed. 

Docker versions supported:

* 1.7.0
* 1.7.1
* 1.8.0
* 1.8.1
* 1.9.0
* 1.9.1
* 1.10.0
* 1.10.1
* 1.10.3

You can pull a specific version of this pipeline by using the appropriate tag.

`docker pull quay.io/ucsc_cgl/exome-cgl-pipeline:<supported docker version>--2.0.8`

## Inputs

The CGL exome pipeline requires input files in order to run. These files are hosted on Synapse and can 
be downloaded after creating an account which takes about 1 minute and is free. 

* Register for a [Synapse account](https://www.synapse.org/#!RegisterAccount:0)
* Either download the samples from the [website GUI](https://www.synapse.org/#!Synapse:syn5886029) or use the Python API
* `pip install synapseclient`
* `python`
    * `import synapseclient`
    * `syn = synapseclient.Synapse()`
    * `syn.login('foo@bar.com', 'password')`
    * Get the Reference Genome (3 G)
        * `syn.get('syn6128232', downloadLocation='.')`
    * Get the Phase VCF (0.3 G)
        * `syn.get('syn6128233', downloadLocation='.')`
    * Get the Mills VCF (0.1 G)
        * `syn.get('syn6128236', downloadLocation='.')`
    * Get the DBSNP VCF (10 G)
        * `syn.get('syn6128237', downloadLocation='.')`
    * Get the Cosmic VCF (0.01 G)
        * `syn.get('syn6128235', downloadLocation='.')`

## Running

Type `docker run quay.io/ucsc_cgl/exomevar-cgl-pipeline` to see a help menu and list of possible run options.

The preferred way to run this pipeline is to colocate the pipeline and sample inputs in the location from which
the pipeline will be run. This greatly simplifies the command line and complexity of running the container.
This location must have _plenty_ of storage, as Toil's job store and temp directories will be created
at this location during run time. A safe estimate for a single sample would be about 100 Gigabytes.

 `-v /var/run/docker.sock:/var/run/docker.sock` must **always** be supplied as Docker argument 
 (see bottom of README for details). 

The work directory, where temp files will be created, must be "mirror mounted". This means that the diretory
must be the same on both sides of the colon in Docker's `-v` command.  

### Example Command

`cd` to the directory where the pipeline inputs and samples are located, then type:

```
docker run \
    -v $(pwd):$(pwd) \ # Work directory
    -v /var/run/docker.sock:/var/run/docker.sock \ # Required Docker socket
    quay.io/ucsc_cgl/exomevar-cgl-pipeline \ # Name of the pipeline
    --normal $(pwd)/normal.bam \
    --tumor $(pwd)/tumor.bam...
```

### Separate sample, input, and work directory locations

If your samples (and/or inputs) are located in a different location than where you would like
the job store and work directories to be created, use the following format:

* Mirror mount points for the work directory: e.g. `-v /foo/bar:/foo/bar`
* Use `-v /foo/bar/samples:/samples`, where `:/samples` is the preferred destination path.
* Use `-v /foo/bar/inputs:/inputs`, where `:/inputs` is the preferred destination path.

Due to the way Docker works, this will change how you supply paths to the samples and inputs. Look at the 
following example and you'll see that the path being passed to the container for samples is no longer 
**/path/to/data/normal.bam**, but **/samples/normal.bam**.  Likewise, the inputs are now passed in
as **/inputs/cosmic.hg19.vcf**. 

```
docker run \
    -v /scratch:/scratch \ # Path to work directory, mirrored
    -v /path/to/data:/samples \ # Path to samples, not mirrored
    -v /path/to/inputs:/inputs \ # Path to inputs, not mirrored
    -v /var/run/docker.sock:/var/run/docker.sock \
    quay.io/ucsc_cgl/exomevar-cgl-pipeline \
    --reference /inputs/reference.hg19.fa \
    --phase /inputs/phase.hg19.vcf \
    --mills /inputs/mills.indels.hg19.sites.vcf \
    --dbsnp /inputs/dbsnp.hg19.vcf \
    --cosmic /inputs/cosmic.hg19.vcf \
    --normal /samples/normal.bam \
    --tumor /samples/tumor.bam...
```

## Core Limit and Restarting

By default, the pipeline will use all available cores on the machine in which it is run. This can be regulated
by using the `--cores` argument.

In the event of failure the pipeline can be resumed by rerunning the pipeline with the `--resume` argument. 

If you would like to inspect the contents of the temp directory, you can specify the `--no-clean` flag.

## Genomic tool containers
The individual tools in the pipeline can be pulled with the following commands:
```
docker pull quay.io/ucsc_cgl/gatk:3.5--dba6dae49156168a909c43330350c6161dc7ecc2
docker pull quay.io/ucsc_cgl/muse:1.0--6add9b0a1662d44fd13bbc1f32eac49326e48562
docker pull quay.io/ucsc_cgl/mutect:1.1.7--e8bf09459cf0aecb9f55ee689c2b2d194754cbd3
docker pull quay.io/ucsc_cgl/pindel:0.2.5b6--4e8d1b31d4028f464b3409c6558fb9dfcad73f88
```
## Into the Weeds

/var/run/docker.sock needs to be mirror mounted so that the host daemon process can spawn sibling containers when
Docker is executed by the parent container as opposed to nesting Docker containers as children which is ill-advised.

The mirror mount for the work directory is required since the Docker call executed inside the parent container
is actually run by the host, meaning the "src" provided to "-v" is actually on the host, not the parent container.

When using multiple mount points, A non-mirrored destination is required because there isn't an easy way to
ascertain which of the mount points is the work path versus sample path. That's because the JSON
returned by Docker inspect isn't ordered.  

You can use whatever mount point you like for the samples and inputs _so long as they are not mirrored_ and
you are consistent about using the destination path when passing in arguments to the container.
