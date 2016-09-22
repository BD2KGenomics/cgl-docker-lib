build_tool = runtime-container.DONE
name = quay.io/ucsc_cgl/s3am
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../s3am | cut -f1 -d " ")
tag = 2.0--${git_commit}

build: ${build_output} ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
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
	docker rmi ${name}:${tag}
