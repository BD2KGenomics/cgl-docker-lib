build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
nametag = quay.io/ucsc_cgl/picardtools:1.95--${git_commit}

all: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${nametag} .
	touch ${build_tool}
