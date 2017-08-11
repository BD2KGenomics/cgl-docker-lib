build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-common ../apache-spark-worker | cut -f1 -d " ")
nametag = quay.io/ucsc_cgl/apache-spark-worker:1.6.3--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile run-worker.sh
	# has apache-spark-common been built yet? if not, build it
	# if it has been built, this command won't do anything.
	cd ../apache-spark-common && $(MAKE) build
	
	# build the runtime container
	docker build -t ${nametag} .
	touch ${build_tool}

clean:
	rm -rf ${build_tool}
	docker rmi -f ${nametag}

test: build

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}
