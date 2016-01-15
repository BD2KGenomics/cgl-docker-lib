# Definitions
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../rsem-1.1.13 | cut -f1 -d " ")
name = quay.io/ucsc_cgl/rsem
tag = 1.1.13--${git_commit}

build:
	docker build -t ${name}:${tag} .
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}

test: build
	python test.py

clean:
	-rm ${build_tool}
