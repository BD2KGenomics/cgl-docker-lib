build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
nametag = computationalgenomicslab/picardtools:1.95--deb--unstable--${git_commit}--${build_number}

all: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${nametag} .
	touch ${build_tool}
