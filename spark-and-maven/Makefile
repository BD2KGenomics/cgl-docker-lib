# Definitions
build_tool = runtime-container.DONE
build_path = build
runtime_path = runtime
nametag = quay.io/ucsc_cgl/spark-and-maven:1.5.2.3.3.9

# Steps
build: ${build_tool}

${build_tool}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${nametag} .
	touch ${build_tool}

clean:
	rm ${build_tool}
	docker rmi -f ${nametag}

test: build

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}
