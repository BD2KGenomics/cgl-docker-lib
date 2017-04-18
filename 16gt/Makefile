build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../platypus | cut -f1 -d " ")
name = quay.io/ucsc_cgl/16gt
tag = 4d894ad188674494dd7f05fc68b0aed90dcf5d1e--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build test.py
	python test.py

clean:
	-rm ${build_tool}
