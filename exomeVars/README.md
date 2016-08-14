# Computational Genomics Lab, Genomics Institute, UC Santa Cruz
### Running the CGL Bam Alignment Pipeline Container

This guide will walk through running the pipeline from start to finish. If you find any errors or corrections please feel free to make a pull request.
Feedback of any kind is appreciated.

## Overview

This container runs the 
[CGL bam alignment pipeline](https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/bwa_alignment), which
is built using [Toil](https://github.com/BD2KGenomics/toil), a high-performance pipeline architecture platform for
running workflows. This container is designed to run local samples.
The BWA pipeline requires input files in order to run. The only required input, aside from the sample(s), is a 
reference genome.

This pipeline requires a host with Docker installed.

## Inputs

The CGL RNA-seq pipeline requires input files in order to run. These files are hosted on Synapse and can 
be downloaded after creating an account which takes about 1 minute. 

* Register for a [Synapse account](https://www.synapse.org/#!RegisterAccount:0)
* Either download the samples from the [website GUI](https://www.synapse.org/#!Synapse:syn5886029) or use the Python API
* `pip install synapseclient`
* `python`
    * `import synapseclient`
    * `syn = synapseclient.Synapse()`
    * `syn.login('foo@bar.com', 'password')`
    * Get the RSEM reference (1 G)
        * `syn.get('syn5889216', downloadLocation='.')`
    * Get the Kallisto index (2 G)
        * `syn.get('syn5886142', downloadLocation='.')`
    * Get the STAR index (25 G)
        * `syn.get('syn5886182', downloadLocation='.')`


## Running

If samples and inputs are colocated in a place with _plenty_ of storage, simply mirror the absolute path to the
parent directory when using Docker's -v mount command. Toil's job store and temporary directories will be 
created inside this mount point. "-v /var/run/docker.sock:/var/run/docker.sock" must always be supplied. 

To reiterate, the mount for the working directory must match on both sides of the colon - 
an error will be thrown if that is not the case. 

```
docker run \
    -v /foo/bar:/foo/bar \
    -v /var/run/docker.sock:/var/run/docker.sock \
    quay.io/ucsc_cgl/rnaseq-cgl-pipeline \
    --star /foo/bar/starIndex_hg38_no_alt.tar.gz \
    --rsem /foo/bar/rsem_ref_hg38_no_alt.tar.gz \
    --kallisto /foo/bar/kallisto_hg38.idx \
    --samples /foo/bar/sample1.tar /foo/bar/sample2.tar ...
```

### Separate sample, input, and work directory locations

If your samples (and/or inputs) are located in a different location than where you would like
the job store and work directories to be created, use the following format:

* Mirror mount points for the work directory: e.g. `-v /foo/bar:/foo/bar`
* Use `-v /foo/bar/samples:/samples`, where `:/samples` is the preferred destination path.
* Use `-v /foo/bar/inputs:/inputs`, where `:/inputs` is the preferred destination path.

Due to the way Docker works, this will change how you supply paths to the samples and inputs. Look at the 
following example and you'll see that the path being passed to the container for samples is no longer 
**/foo/bar/samples/sample1.tar**, but **/samples/sample1.tar**.  Likewise, the inputs are now passed in
as **/inputs/kallisto_hg38.idx**. 

```
docker run \
    -v /scratch:/scratch \ # Path to work directory, mirrored
    -v /path/to/data:/samples \ # Path to samples, not mirrored
    -v /path/to/inputs:/inputs \ # Path to inputs, not mirrored
    -v /var/run/docker.sock:/var/run/docker.sock \
    quay.io/ucsc_cgl/bam-alignment \
    --ref /inputs/refrence.tar \
    --samples /samples/sample1.tar /samples/sample2.tar ...
```

## Restarting

In the event of failure, the pipeline can be restarted by re-running the Docker command with the `--restart` argument.

## Into the Weeds

/var/run/docker.sock needs to be mirror mounted so that the host daemon process can spawn sibling containers when
Docker is executed by the parent container as opposed to nesting Docker containers as children which is ill-advised.

The mirror mount for the work directory is required since the Docker call executed inside the parent container
is actually run by the host, meaning the "src" provided to "-v" is actually on the host, not the parent container.

When using multiple mount points, A non-mirrored destination is required because there isn't an easy way to
ascertain which of the mount points is the work path versus sample path. That's because the JSON
returned by Docker inspect isn't ordered.  

You can use whatever mount point you like for the samples and inputs _so long as they are not mirrored_ and
you are consistent about using the dst path when passing in arguments to the container.
