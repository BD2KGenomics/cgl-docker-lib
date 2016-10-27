build_tool = runtime-container.DONE
git_commit ?= $(shell git log --pretty=oneline -n 1 -- ../apache-spark-common ../apache-spark-master | cut -f1 -d " ")
nametag = quay.io/ucsc_cgl/apache-spark-master:1.5.2--${git_commit}

build: ${build_tool}

${build_tool}: Dockerfile run-master.sh
	# has apache-spark-common been built yet? if not, build it
	# if it has been built, this command won't do anything.
	cd ../apache-spark-common && make build

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
