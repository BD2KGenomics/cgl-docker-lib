build_tool = runtime-container.DONE
name = quay.io/ucsc_cgl/apache-hadoop-worker
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-hadoop-common ../apache-hadoop-worker | cut -f1 -d " ")
tag = 2.7.4--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile start-worker.sh
	# has apache-hadoop-common been built yet? if not, build it
	# if it has been built, this command won't do anything.
	cd ../apache-hadoop-common && $(MAKE) build
	
	# build the runtime container
	docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

clean:
	rm -rf ${build_tool}
	docker rmi -f ${name}:${tag}

test: build

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
