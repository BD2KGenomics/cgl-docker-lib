build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse head)

all: ${build_tool}

${build_tool}:
	docker build -t computationalgenomicslab/samtools:0.1.19--deb--unstable--${git_commit)--${build_number} .