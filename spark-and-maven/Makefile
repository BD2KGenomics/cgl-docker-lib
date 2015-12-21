# Definitions
build_path = build
runtime_path = runtime
nametag = computationalgenomicslab/spark-and-maven:1.5.2.3.3.3

# Steps
build: ${build_path}/Dockerfile
	cd ${build_path} && docker build -t ${nametag}-build . 

clean:
	docker rmi -f ${nametag}-build

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}
