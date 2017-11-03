FROM quay.io/ucsc_cgl/apache-hadoop-common:2.6.2

MAINTAINER Alyssa Morrow, akmorrow@berkeley.edu

# copy jar
RUN mkdir /opt/cgl-docker-lib
COPY mango /opt/cgl-docker-lib/mango

# copy spark
COPY apache-spark /opt/cgl-docker-lib/apache-spark

ENV SPARK_HOME /opt/cgl-docker-lib/apache-spark

# put mango jar on the pyspark path for packaging
ENV ASSEMBLY_DIR /opt/cgl-docker-lib/mango/mango-assembly/target
ENV ASSEMBLY_JAR "$(ls -1 "$ASSEMBLY_DIR" | grep "^mango-assembly[0-9A-Za-z\_\.-]*\.jar$" | grep -v javadoc | grep -v sources || true)"
ENV PYSPARK_SUBMIT_ARGS "--jars ${ASSEMBLY_DIR}/${ASSEMBLY_JAR} --driver-class-path ${ASSEMBLY_DIR}/${ASSEMBLY_JAR} pyspark-shell"

# set env variables for python path TODO RM
ENV PYTHONPATH ${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.4-src.zip

#environment variables PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON
ENV PYSPARK_PYTHON /usr/bin/python
ENV  PYSPARK_DRIVER_PYTHON /usr/bin/python


# Install make and pip/python dependencies
RUN apt-get update && apt-get install -y \
  git \
  make \
  python-pip \
  npm \
  nodejs \
  python-tk

RUN ln -s /usr/bin/nodejs /usr/bin/node

# set permissions for running npm. Required for mango-viz
RUN npm config set bdgenomics.mango.pileup:unsafe-perm

# prepare mango-viz and mango-python
WORKDIR /opt/cgl-docker-lib/mango/mango-python
RUN make prepare && make develop

WORKDIR /opt/cgl-docker-lib/mango/mango-viz
RUN make prepare && make develop

WORKDIR /

# by default, runs mango browser (mango-submit)
# to override to mango-notebook,
# run docker with --entrypoint=/opt/cgl-docker-lib/mango/bin/mango-notebook
ENTRYPOINT ["/opt/cgl-docker-lib/mango/bin/mango-submit"]
