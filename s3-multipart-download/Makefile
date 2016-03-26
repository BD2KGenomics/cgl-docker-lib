# Definitions
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../s3-multipart-download | cut -f1 -d " ")
name = quay.io/ucsc_cgl/s3-multipart-download
tag = 98b5b01--${git_commit}

build:
	docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
