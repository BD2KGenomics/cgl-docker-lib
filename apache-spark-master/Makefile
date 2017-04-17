build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-master | cut -f1 -d " ")
nametag = quay.io/ucsc_cgl/apache-spark-master:1.6.3--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile run-master.sh
	docker build -t ${nametag} .
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}

test: build
