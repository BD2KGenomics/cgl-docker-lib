# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/apache-spark
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-common | cut -f1 -d " ")
name = quay.io/ucsc_cgl/apache-spark-common
tag = 1.5.2--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -no-cache -t ${name}-build:${tag} . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile 
	cd ${runtime_path} && docker build -t ${name}:${tag} .
	touch ${build_tool}

test: build

clean:
	rm -rf runtime/apache-spark ${build_tool}
	docker rmi -f ${name}-build:${tag} ${name}:${tag}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
