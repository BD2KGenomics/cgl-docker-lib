# Definitions
build_path = build/
runtime_path = runtime/
build_output = ${runtime_path}/mutect-1.1.7.jar
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
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
