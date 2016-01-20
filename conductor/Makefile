# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/adam
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
nametag = quay.io/ucsc_cgl/conductor:latest

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${nametag}-build . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${nametag}-build cp -r /home/conductor /data/conductor
	docker run -v ${runtime_fullpath}:/data ${nametag}-build cp -r /opt/apache-spark /data/apache-spark

${build_tool}: ${build_output} ${runtime_path}/Dockerfile
	cd ${runtime_path} && docker build -t ${nametag} .
	touch ${build_tool}

test: build

clean:
	docker rmi -f ${nametag}-build
	rm -rf ${runtime_fullpath}/conductor ${runtime_fullpath}/apache-spark

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}
