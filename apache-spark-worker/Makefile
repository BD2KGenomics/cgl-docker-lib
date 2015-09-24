build_tool = runtime-container.DONE
nametag = computationalgenomicslab/apache-spark-worker:1.5.0

all: ${build_tool}

${build_tool}: Dockerfile run-worker.sh
	docker build -t ${nametag} .
	touch ${build_tool}
