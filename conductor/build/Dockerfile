FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y \
	git \
	openjdk-7-jdk \
	python \
	libnss3 \
	curl

COPY download.sh /home/
RUN sh /home/download.sh

ENV PATH /opt/apache-spark/bin:$PATH

WORKDIR /home

# clone conductor
RUN git clone https://github.com/BD2KGenomics/conductor.git

# build conductor
WORKDIR /home/conductor
RUN git pull --commit \
    https://github.com/fnothaft/conductor.git \
    hadoop-version

RUN /opt/apache-maven-3.3.3/bin/mvn package \
    -DskipTests \
    -Dhadoop.version=2.6.0 \
    -Dspark.version=1.5.2



