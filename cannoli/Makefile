# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/cannoli
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../spark-and-maven ../cannoli ../adam | cut -f1 -d " ")
name = quay.io/ucsc_cgl/cannoli
tag = 122ead2219b987bb60e5f108a2d261e056abc86e--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ../spark-and-maven && $(MAKE) build
	cd ${build_path} && docker build --no-cache -t ${name}-build:${tag} . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /home/cannoli /data/cannoli
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile 
	#cd ../adam && $(MAKE) build
	cd ${runtime_path} && docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

test: build
	python test.py

clean:
	rm -rf runtime/cannoli runtime/apache-spark ${build_tool}
	docker rmi -f ${name}-build:${tag} ${name}:${tag}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
