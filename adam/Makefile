# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/adam
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
nametag = computationalgenomicslab/adam:latest

# Steps
all: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${nametag}-build . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${nametag}-build cp -r /home/adam /data/adam
	docker run -v ${runtime_fullpath}:/data ${nametag}-build cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile
	cd ${runtime_path} && docker build -t ${nametag} .
	touch ${build_tool}

clean:
	docker rmi -f ${nametag}-build

push: all
	# Requires ~/.dockercfg 
	docker push ${nametag}
