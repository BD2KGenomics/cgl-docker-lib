# Definitions
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../spladder | cut -f1 -d " ")
name = quay.io/ucsc_cgl/spladder
tag = 732349f6dd0df3fb90fa9d7e6ee1e04a32e2e773--${git_commit}

build:
	docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build

clean:
	-rm ${build_tool}