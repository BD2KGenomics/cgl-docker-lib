# Definitions
build_output = runtime/cmake
runtime_fullpath = $(realpath runtime)
build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../cmake | cut -f1 -d " ")
name = quay.io/ucsc_cgl/cmake
shorttag = 3.9.1
tag = ${shorttag}--${git_commit}


# Steps
build:
	docker build -t ${name}:${tag} .
	-docker rmi -f ${name}:latest
	docker tag ${name}:${tag} ${name}:latest
	-docker rmi -f ${name}:${shorttag}
	docker tag ${name}:${tag} ${name}:${shorttag}
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:${shorttag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm ${build_output}
