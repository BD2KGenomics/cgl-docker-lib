build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse head)

all: ${build_tool}

${build_tool}: Dockerfile
	docker build -t quay.io/ucsc_cgl/ubu:1.2--${git_commit}
	touch ${build_tool}
