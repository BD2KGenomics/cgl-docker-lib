build_tool = runtime-container.DONE
git_commit ?= $(shell git rev-parse HEAD)
name = quay.io/ucsc_cgl/rnaseqc
tag = 1.1.8--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${name}:${tag} .
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:{tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
