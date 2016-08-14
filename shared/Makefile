# Definitions
build_tool = .runtime-container.DONE
name = quay.io/ucsc_cgl/${name}
tag = 2.0.8

build: ${build_tool}

${build_tool}: Dockerfile-template.py
	python Dockerfile-template.py ${name} ${tag} build
	touch ${build_tool}

push: build
	# Requires ~/.dockercfg
	python Dockerfile-template.py ${name} ${tag} push

test: build
	python test.py ${tag}

clean:
	-rm ${build_tool}
