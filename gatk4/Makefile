# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/gatk
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../gatk4 ../spark-and-maven | cut -f1 -d " ")
name = quay.io/ucsc_cgl/gatk4
tag = c655fef1221615af753bd37590da2c7550ae72b0--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ../spark-and-maven && $(MAKE) build
	cd ${build_path} && docker build -t ${name}-build:${tag} . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /home/gatk/build/gatk-4.beta.3-36-gc655fef-SNAPSHOT.zip /data/gatk.zip
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile 
	cd ${runtime_path} && docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

test: build
	python test.py

clean:
	rm -rf runtime/gatk runtime/apache-spark ${build_tool}
	docker rmi -f ${name}-build:${tag} ${name}:${tag}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
