Containerization Standards for Tools in Docker
====================

Basic Philosophy
---------------------

The goal of encapsulating a genomics tool in a Docker container is to create 
a modular, portable tool that is software agnostic and can run on almost any hardware. 
The tool should be setup such that the call to the tool only requires the appended arguments 
prepended by the standard Docker boilerplate:

    docker run quay.io/ucsc_cgl/<Tool> [Parameters]

1. The Docker image should contain only the tool and the minimum dependencies needed to run that tool.
2. The tool should be launched when the person runs the image without needing to know where the tool is located or how it is called. If no parameters are passed, the user should be presented with the tool's help menu.
3. All images should have a folder **/data** that acts as the standard mount point. The final working directory in the container should be set to **/data** (`WORKDIR /data`). 
4. Any scripts, jars, wrappers or other software should go in **/opt/\<tool name\>**
5. More complex tools with many build dependencies should follow the guidelines in **Complex Tools**.  The general idea is to separate the build dependencies from runtime dependencies minimizing the final size of the deployed image.
6. Building a tool from source should only require changing to the tool’s directory and typing make. All built images should conform to the tag standards set in section **Tag Conventions**.
7. Every image should have an `ENTRYPOINT` set to a wrapper script. (see **Wrapper Script**)   
8. All tools should be lowercase in the github repo and follow the directory structure outlined in the figure below. In this figure, **samtools** is a basic tool, while **bwa** is a *complex tool*. 

<p align="center">
<img align="center" src="http://i.imgur.com/j4kracV.png" width="400"#dir  />
</p>


Dockerfile Structure
---------------------
The de-facto guide to follow is available [on Docker's website](https://docs.docker.com/articles/dockerfile_best-practices/).

Useful highlights:

1. Don't do `RUN apt-get update` on a single line. Pair with `apt-get install` using `&&`. This is due to issues with how Docker caches.
3. `CD` does not work intuitively. Use `WORKDIR` (absolute path).
4. Always attempt to launch the tool via `ENTRYPOINT`. Always use the "exec" form, e.g. `["foo", "bar"]`

### Complex Tools
A *complex tool* is a tool that requires several build dependencies and fewer (or different) runtime dependencies.
In the end, it is up to the developer to decide whether or not a tool should conform to the standards 
we set for a complex tool, but if the end size of the image can be reduced or unneeded build dependencies 
can be eliminated, it is preferred. An example of a Makefile that orchestrates that is below:

```
# Definitions
build_output = runtime/gatk.jar
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../gatk | cut -f1 -d " ")
name = quay.io/ucsc_cgl/gatk
tag = 3.4--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t gatkbuild .
	docker run -v ${runtime_fullpath}:/data gatkbuild cp gatk.jar /data

${build_tool}: ${build_output} runtime/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	docker rmi -f gatkbuild
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm ${build_output}
```

## Tag Conventions
Tags will be used in two ways: to record information about that particular build of the image and for easy deployment.  Our group uses Jenkins for continuous integration of the project and conforms to the following tag standard:

1. `${ToolVersion}--${MostRecentCommitHashForTool}`

### Latest Tag and Version Tag
In an effort to make the software as accessible as possible, every tool should have a `latest` tag associated with at least one image of that tool. Since our group now uses the Docker hosting site [Quay.io](www.quay.io), tags are visually linked by hash so one can always determine which commit is associated with the `latest` tag.

## Branches
All tools should be on their own branch while under development.  Once a tool is ready, that branch should be rebased to the **Master** and pull request submitted.  

## Wrapper Script
Every image should have a wrapper script set as the `ENTRYPOINT` which handles launching the tool (with parameters), and importantly, changing the ownership of all output files to the owner of the mounted **/data** directory.  This wrapper script allows for all kinds of flexibility, as the example below shows the wrapper script handling ownership of output files from root to the host user as well as using environment variables to allow any number of java options to be passed during jar execution. An example of a wrapper script for gatk is shown below:
```
#!/usr/bin/env bash
# Call tool with parameters
java $JAVA_OPTS -jar /opt/cgl-docker-lib/gatk.jar "$@"
# Fix ownership of output files
UID=$(stat -c '%u:%g' /data)
chown -R $UID /data
```

## Standards Within the Genomics Community

GA4GH members have agreed to begin work on creating standards for dockerizing genomics tools.  Once that has happened, this document and repository will be updated to comply.
