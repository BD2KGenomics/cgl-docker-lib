# Definitions
build_tool = runtime-container.DONE
build_path = build
runtime_path = runtime
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../spark-and-maven | cut -f1 -d " ")
name = quay.io/ucsc_cgl/spark-and-maven
tag = 2.1.0.3.3.9--${git_commit}

# Steps
build: ${build_tool}

${build_tool}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

clean:
	rm ${build_tool}
	docker rmi -f ${name}:${tag}

test: build

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
