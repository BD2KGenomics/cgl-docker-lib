# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/adam
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
name = quay.io/ucsc_cgl/adam
tag = c251f79c6bde3dce12e685c6cf03d5b1c30e9273--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -no-cache -t ${name}-build:${tag} . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /home/adam /data/adam
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile 
	cd ${runtime_path} && docker build -t ${name}:${tag} .
	touch ${build_tool}

test: build
	python test.py

clean:
	rm -rf runtime/adam runtime/apache-spark ${build_tool}
	docker rmi -f ${name}-build:${tag} ${name}:${tag}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
