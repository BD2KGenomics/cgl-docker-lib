# Definitions
build_path = build
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-common | cut -f1 -d " ")
name = quay.io/ucsc_cgl/apache-spark-common
tag = 1.6.3--${git_commit}

# Steps
build: ${build_tool}

${build_tool}: Dockerfile 
	docker build -t ${name}:${tag} .
	touch ${build_tool}

test: build

clean:
	docker rmi -f ${name}:${tag}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
