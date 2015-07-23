build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse head)

all: ${build_tool}

${build_tool}: Dockerfile
	docker build -t computationalgenomicslab/ubu:1.2--src--unstable--${git_commit}--${build_number} .
	touch ${build_tool}
