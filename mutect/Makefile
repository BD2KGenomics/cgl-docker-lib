# Definitions
build_output = build/mutect-1.1.7.jar
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../mutect | cut -f1 -d " ")
name = quay.io/ucsc_cgl/mutect
tag = 1.1.7--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t mutectbuild . 
	docker run -v ${runtime_fullpath}:/data mutectbuild cp mutect-1.1.7.jar /data

${build_tool}: ${build_output} build/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	docker rmi -f mutectbuild
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm -r ${build_output}
