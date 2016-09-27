# Definitions
build_path = build
runtime_path = runtime
build_output = ${runtime_path}/adam
runtime_fullpath = $(realpath ${runtime_path})
build_tool = runtime-container.DONE
build_number ?= none
git_commit ?= $(shell git rev-parse HEAD)
name = quay.io/ucsc_cgl/quinine
tag = a987006fdf38afadc9c6a22061885f8e105234f7--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${name}-build:${tag} . 
	echo ${runtime_fullpath}
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /home/quinine /data/quinine

${build_tool}: ${build_output} ${runtime_path}/Dockerfile 
	cd ${runtime_path} && docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

test: build
	python test.py

clean:
	rm -rf runtime/quinine ${build_tool}
	docker rmi -f ${name}-build:${tag} ${name}:${tag}

print_tag:
	@echo ${tag}

push: build
	# Requires ~/.dockercfg 
	docker push ${name}:${tag}
	docker push ${name}:latest
