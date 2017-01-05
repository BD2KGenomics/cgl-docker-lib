build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../gencode_hugo_mapping | cut -f1 -d " ")
name = quay.io/ucsc_cgl/gencode_hugo_mapping
tag = 1.0--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${name}:${tag} .
	docker tag ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build

clean:
	-rm ${build_tool}
