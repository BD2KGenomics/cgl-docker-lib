# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/conductor
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../spark-and-maven ../avocado | cut -f1 -d " ")
name = quay.io/ucsc_cgl/conductor
tag = fnothaft--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ../spark-and-maven && $(MAKE) build
	cd ${build_path} && docker build -t ${name}:${tag}-build . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${name}:${tag}-build cp -r /home/conductor /data/conductor
	docker run -v ${runtime_fullpath}:/data ${name}:${tag}-build cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile
	cd ${runtime_path} && docker build -t ${name}:${tag} .
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

test: build test.py
	python test.py

clean:
	docker rmi -f ${name}:${tag}-build
	rm -rf ${runtime_fullpath}/conductor ${runtime_fullpath}/apache-spark

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
