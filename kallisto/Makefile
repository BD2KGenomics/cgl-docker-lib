build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse head)
nametag = computationalgenomicslab/kallisto:0.42.2.1--deb--unstable--${git_commit}--${build_number}

all: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${nametag} .
	touch ${build_tool}
