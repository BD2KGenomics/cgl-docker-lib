# Definitions
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../quinine-pipelines | cut -f1 -d " ")
name = quay.io/ucsc_cgl/quinine-pipelines
tag = 716dd26cf6252a6db60afa25aaf7cf9ee9896b21--${git_commit}

workflows = contamination.workflow.json rna.workflow.json targeted.workflow.json

build:
	docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build ${workflows}
	python test.py -b

%.workflow.json: %.workflow.json.template
	sed -e "s:PWD:${PWD}:g" $< > $@

clean:
	-rm ${build_tool} *.workflow.json
