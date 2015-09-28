build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
nametag = computationalgenomicslab/tachyon-master:0.7.1

all: ${build_tool}

${build_tool}: Dockerfile start-tachyon-master.sh
	docker build -t ${nametag} .
	touch ${build_tool}
