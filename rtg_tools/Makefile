# Definitions
build_output = runtime/rtg-tools.jar
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../rtg_tools | cut -f1 -d " ")
name = quay.io/ucsc_cgl/rtg_tools
tag = 3.8.3--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t rtgtoolsbuild .
	docker run -v ${runtime_fullpath}:/data rtgtoolsbuild cp /home/rtgtools-protected/rtg-tools.jar /home/rtgtools-protected/LICENSE.txt /data

${build_tool}: ${build_output} runtime/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	-docker rmi ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	-docker rmi -f rtgtoolsbuild
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
