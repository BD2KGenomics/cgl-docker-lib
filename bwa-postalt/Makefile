# Definitions
runtime_fullpath = $(realpath runtime)
name = quay.io/ucsc_cgl/bwa-postalt
tag = 0.7.12
build_output = runtime/bwa-postalt.js
build_tool = runtime-container.DONE

# Steps
build: ${build_output} ${build_tool}

${build_output}: build/Dockerfile
	cd build && docker build -t ${name}-build:${tag} .
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp /home/bwa/bwakit/bwa-postalt.js /data/bwa-postalt.js
	docker run -v ${runtime_fullpath}:/data ${name}-build:${tag} cp -r /home/k8 /data/k8

${build_tool}: ${build_output} runtime/Dockerfile
	cd runtime && docker build -t ${name}:${tag} .
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	docker rmi ${name}-build:${tag}
	docker rmi ${name}:${tag}
	rm -rf ${build_tool} ${build_output} runtime/k8
