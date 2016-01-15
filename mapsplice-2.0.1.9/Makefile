# Definitions
build_output = runtime/MapSplice-v2.1.8
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../mapsplice-2.0.1.9 | cut -f1 -d " ")
name = quay.io/ucsc_cgl/mapsplice
tag = 2.0.1.9--${git_commit}

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t mapsplicebuild . 
	docker run -v ${runtime_fullpath}:/data mapsplicebuild cp -r MapSplice_multi_threads_2.0.1.9 /data

${build_tool}: ${build_output} runtime/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	docker rmi -f mapsplicebuild
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm -r ${build_output}