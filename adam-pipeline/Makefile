# Definitions
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../rnaseq-cgl-pipeline | cut -f1 -d " ")
name = quay.io/ucsc_cgl/adam-pipeline
tag = f7512d5ac3bcaa40fa2682236c2f1b44020a2861--${git_commit}

build:
	docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build workflow.json
	python test.py -b

workflow.json: workflow.json.template
	sed -e "s:PWD:${PWD}:g" workflow.json.template > workflow.json

clean:
	-rm ${build_tool} workflow.json
