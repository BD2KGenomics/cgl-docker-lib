# Definitions
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
name = quay.io/ucsc_cgl/spooky_test
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../spooky-test | cut -f1 -d " ")
tag = 1.0.0a--${git_commit}

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
