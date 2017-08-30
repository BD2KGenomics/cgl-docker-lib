# Definitions
build_output = runtime/hera
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../hera | cut -f1 -d " ")
name = quay.io/ucsc_cgl/hera
tag = 1.1--${git_commit}

# Steps
build:
	docker build -t ${name}:${tag} .
	-docker rmi -f ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm ${build_output}
