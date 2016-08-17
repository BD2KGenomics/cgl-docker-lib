# Definitions
docker_versions = 1.7.0 1.7.1 1.8.0 1.8.1 1.9.0 1.9.1 1.10.0 1.10.1 1.10.3
gen_directories = $(docker_versions:=.docker)

build: ${build_tool}

%.docker: dockerver=$(@:.docker=)
%.docker: Dockerfile.template Makefile.template
	mkdir -p $@
	sed -e "s:DOCKERVER:${dockerver}:g" Dockerfile.template > ${@}/Dockerfile
	sed -e "s:DOCKERVER:${dockerver}:g" Makefile.template > ${@}/Makefile
	cd $@ && ln -sf ../test.py

generate: ${gen_directories}

${build_tool}: generate
	$(foreach subdir, $(gen_directories), cd $(subdir) && $(MAKE) build)

push: build
	# Requires ~/.dockercfg
	$(foreach subdir, $(gen_directories), cd $(subdir) && $(MAKE) push)

test: build test.py
	$(foreach subdir, $(gen_directories), cd $(subdir) && $(MAKE) test)

clean:
	$(foreach subdir, $(gen_directories), cd $(subdir) && $(MAKE) clean)
	-rm -rf ${gen_directories}
