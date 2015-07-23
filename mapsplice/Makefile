# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/MapSplice-v2.1.8
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)

# Steps
all: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t mapsplicebuild . 
	docker run -v ${runtime_fullpath}:/data mapsplicebuild cp -r MapSplice-v2.1.8 /data

${build_tool}: ${build_output} ${runtime_path}/Dockerfile
	cd ${runtime_path} && docker build -t computationalgenomicslab/mapsplice:2.1.8--src--unstable--${git_commit}--${build_number} .
	docker rmi -f mapsplicebuild
	touch ${build_tool}

push: all
	# Requires ~/.dockercfg 
	docker push computationalgenomicslab/mapsplice:2.1.8--src--unstable--${git_commit}--${build_number}
