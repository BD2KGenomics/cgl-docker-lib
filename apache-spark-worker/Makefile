build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-worker | cut -f1 -d " ")
nametag = quay.io/ucsc_cgl/apache-spark-worker:2.1.1--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile run-worker.sh
	docker build -t ${nametag} .
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}

test: build
