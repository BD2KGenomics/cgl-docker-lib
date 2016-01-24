build_tool = runtime-container.DONE
nametag = quay.io/ucsc_cgl/bwakit:0.7.12

build: ${build_tool}

${build_tool}: Dockerfile
	docker build -t ${nametag} .
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg 
	docker push ${nametag}

test: build
	python test.py

clean:
	-rm ${build_tool}
	docker rmi ${nametag}
