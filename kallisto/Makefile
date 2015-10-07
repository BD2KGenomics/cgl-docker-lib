# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/kallisto
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
nametag = quay.io/ucsc_cgl/kallisto:0.42.2.1--src--unstable--${git_commit}--${build_number}

# Steps
all: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t kallistobuild . 
	docker run -v ${runtime_fullpath}:/data kallistobuild cp kallisto /data

${build_tool}: ${build_output} ${runtime_path}/Dockerfile
	cd ${runtime_path} && docker build -t ${nametag} .
	docker rmi -f kallistobuild
	touch ${build_tool}

push: all
	# Requires ~/.dockercfg 
	docker push ${nametag}