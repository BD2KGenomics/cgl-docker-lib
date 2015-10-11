# Definitions
build_output = runtime/MapSplice-v2.1.8
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git rev-parse HEAD)
name = quay.io/ucsc_cgl/mapsplice
tag = 2.1.8--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t mapsplicebuild . 
	docker run -v ${runtime_fullpath}:/data mapsplicebuild cp -r MapSplice-v2.1.8 /data

${build_tool}: ${build_output} runtime/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	docker rmi -f mapsplicebuild
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