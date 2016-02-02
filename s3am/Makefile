# Definitions
build_tool = runtime-container.DONE
name = quay.io/ucsc_cgl/s3am
tag = 1.0a1

# Steps
build: ${build_output} ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${name}:${tag} .
	docker tag -f ${name}:${tag} ${name}:latest
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	docker push ${name}:${tag}
	docker push ${name}:latest

test: build
	python test.py

clean:
	-rm ${build_tool}
	-rm ${build_output}
	docker rmi ${name}:${tag}
