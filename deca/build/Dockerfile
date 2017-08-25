FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone deca
RUN git clone https://github.com/mlinderm/deca.git

# build deca
WORKDIR /home/deca
RUN git checkout ea74eb84322ea120a1fc8d1fa5b50b094d86da73

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
