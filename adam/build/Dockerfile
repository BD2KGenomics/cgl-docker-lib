FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y \
	git \
	openjdk-7-jdk \
	python \
	libnss3 \
	curl

ADD download.sh
RUN download.sh

ENV PATH /opt/apache-spark/bin:$PATH

WORKDIR /home

# clone adam
RUN git clone https://github.com/bigdatagenomics/adam.git

# build adam
WORKDIR /home/adam
RUN /opt/apache-maven-3.3.3/bin/mvn package -DskipTests



