build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-worker | cut -f1 -d " ")
name = quay.io/ucsc_cgl/apache-spark-worker
tag = 2.1.1--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile run-worker.sh
	docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
