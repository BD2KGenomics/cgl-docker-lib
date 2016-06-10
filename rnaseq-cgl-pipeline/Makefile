# Definitions
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../rnaseq-cgl-pipeline | cut -f1 -d " ")
name = quay.io/ucsc_cgl/rnaseq-cgl-pipeline
tag = 2.0.8

build: ${build_tool}

${build_tool}: Dockerfile-template.py
	python Dockerfile-template.py ${name} ${tag} build
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	python Dockerfile-template.py ${name} ${tag} push

test: build
	python test.py ${tag}

clean:
	-rm ${build_tool}
