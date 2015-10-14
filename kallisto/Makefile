# Definitions
build_output = runtime/kallisto
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../kallisto | cut -f1 -d " ")
name = quay.io/ucsc_cgl/kallisto
tag = 0.42.2.1--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t kallistobuild . 
	docker run -v ${runtime_fullpath}:/data kallistobuild cp kallisto /data

${build_tool}: ${build_output} runtime/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	docker rmi -f kallistobuild
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm ${build_output}