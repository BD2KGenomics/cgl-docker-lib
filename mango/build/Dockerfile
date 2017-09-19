FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Alyssa Morrow, akmorrow@berkeley.edu

# Make port 8080 available for mango browser
EXPOSE 8080
# Make port 8888 available for mango notebook
EXPOSE 8888

WORKDIR /home

# clone mango
RUN git clone https://github.com/bigdatagenomics/mango.git
ENV MAVEN_OPTS "-Xmx2g"

# build mango
WORKDIR /home/mango

RUN ./scripts/move_to_spark_2.sh
RUN ./scripts/move_to_scala_2.11.sh

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests

# remove git libraries to avoid permission errors when copying
RUN rm -rf /home/mango/.git

WORKDIR /home/mango
