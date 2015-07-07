# Definitions
build_path = build/
runtime_path = runtime/
build_output = ${runtime_path}/mutect-1.1.7.jar
runtime_fullpath = $(realpath ${runtime_path})
build_tool = DONE

# Steps
all: ${build_output} ${build_tool}

${build_output}:
	cd ${build_path} && docker build -t mutectbuild . 
	docker run -v ${runtime_fullpath}:/data mutectbuild cp mutect-1.1.7.jar /data

${build_tool}: ${build_output}
	cd ${runtime_path} && docker build -t computationalgenomicslab/mutect:1.1.7 . 
	docker rmi -f mutectbuild
	touch ${build_tool}

push: all
	# Requires ~/.dockercfg 
	docker push computationalgenomicslab/mutect:1.1.7
