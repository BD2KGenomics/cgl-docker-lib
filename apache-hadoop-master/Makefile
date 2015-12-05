build_tool = runtime-container.DONE
nametag = computationalgenomicslab/apache-hadoop-master:2.6.2

build: ${build_tool}

${build_tool}: Dockerfile start-master.sh
	# has apache-hadoop-common been built yet? if not, build it
	# if it has been built, this command won't do anything.
	cd ../apache-hadoop-common && make build
	
	# build the runtime container
	docker build -t ${nametag} .
	touch ${build_tool}

clean:
	rm -rf ${build_tool}
	docker rmi -f ${nametag}
