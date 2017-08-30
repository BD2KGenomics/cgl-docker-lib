build_tool = runtime-container.DONE
nametag = quay.io/ucsc_cgl/apache-hadoop-worker:2.7.4

build: ${build_tool}

${build_tool}: Dockerfile start-worker.sh
	# has apache-hadoop-common been built yet? if not, build it
	# if it has been built, this command won't do anything.
	cd ../apache-hadoop-common && $(MAKE) build
	
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
