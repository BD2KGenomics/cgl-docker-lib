Containerization Standards for Tools in Docker
====================


Basic Philosophy
---------------------

The goal of encapsulating a genomics tool in a Docker container is to create 
a modular, portable tool that is software agnostic and can run on almost any hardware. 
The tool should be setup such that the call to the tool only requires the appended arguments 
prepended by the standard Docker boilerplate:

    Docker run <Repo/Tool:tag> [Parameters]

1. The Docker image should contain only the tool and the minimum dependencies needed to run that tool.
2. The tool should be launched when the person runs the image without needing to know where the tool is located or how it is called. 
3. All images should have a folder **/data** and have that folder set as the final `WORKDIR`. 
4. Any scripts, jars, wrappers or other software should go in **/opt/cgl-docker-lib**
5. More complex tools with many build dependencies should follow the guidelines in **Complex Tools**.  The general idea is to separate the build dependencies from runtime dependencies minimizing the final size of the deployed image.
6. Building a tool should only require changing to the tool’s directory and typing make. All built images should conform to the tag standards set in section **Tag Conventions**.
7. All tools should be lowercase in the github repo and follow the directory structure outlined in the figure below. In this figure, **samtools** is a basic tool, while **mutect** is a *complex tool*. 

<p align="center">
<img align="center" src="http://i.imgur.com/ha6WXXT.png" width="400"#dir  />
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
can be eliminated, it is preferred. An example of a Makefile that orchestrates a build image, binary extraction, and runtime image can be seen below.

```
# Definitions
build_path = build/
runtime_path = runtime/
build_output = ${runtime_path}/mutect-1.1.7.jar
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse head)
nametag = computationalgenomicslab/mutect:1.1.7--src--unstable--${git_commit}--${build_number}

# Steps
all: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t mutectbuild . 
	docker run -v ${runtime_fullpath}:/data mutectbuild cp mutect-1.1.7.jar /data

${build_tool}: ${build_output} ${runtime_path}/Dockerfile
	cd ${runtime_path} && docker build -t ${nametag} .
	docker rmi -f mutectbuild
	touch ${build_tool}

push: all
	# Requires ~/.dockercfg 
	docker push ${nametag}
```

## Tag Conventions
Tags will be used in two ways: to record as much information as possible about that particular build of the image and for easy deployment.  Our group uses Jenkins for continuous integration of the project and conforms to the following tag standard.

1. `${upstreamVersion}--${srcType}--stable--${gitReleaseTag}--${jenkinsBuildNumber}`
2. `${upstreamVersion}--${srcType}--unstable--${gitCommit}--${jenkinsBuildNumber}`

| Variable | Meaning |
| :------------ | -----:|
| **upstreamVersion** | The version of the software/tool being containerized |
| **srcType**     | Whether the project was built from src, or pulled (deb, rpm) |
| **(un)stable** | Unstable should be used until a very stable release is ready |
| **gitReleaseTag** | Custom tag for a particular commit |
| **gitCommit** | The commit hash from that particular build | 
| **jenkinsBuildNumber** | Jenkins internal build number |

If a tool is not being built by Jenkins the default for `jenkinsBuildNumber` should be **none**.  
All tools should be built with the unstable tag until ready to be merged into the Release branch 
of the cgl-docker-lib repository.

### Latest Tag and Version Tag
In an effort to make the software as accessible as possible, every tool should have a `latest` tag associated with at least one image of that tool.  It is imperative that the **Information** tab on Dockerhub pair the appropriate long-form tag to the `latest` tag as the latest tag provides no information to the user at all. 
Also paired to each long-form tag should be a “version tag”.  This tag should only list the software version.

## Branches
All tools should be on their own branch while under development.  Once an unstable version is ready, that branch should be rebased to the **Master** and once approved will be merged.  Only fully vetted and stable tools will be merged to the **Release** branch.  The **Release** branch is the only branch from which Jenkins will push tools to our group’s Dockerhub. 

## Standards Within the Docker Community

https://github.com/opencontainers/specs
