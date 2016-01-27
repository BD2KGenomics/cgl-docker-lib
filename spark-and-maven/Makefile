# Definitions
build_tool = runtime-container.DONE
build_path = build
runtime_path = runtime
nametag = quay.io/ucsc_cgl/spark-and-maven:1.5.2.3.3.3

# Steps
build: ${build_tool}

${build_tool}: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${nametag}-build .

clean:
	docker rmi -f ${nametag}-build

test: build

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}
