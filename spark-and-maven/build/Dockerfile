FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y \
	git \
	openjdk-8-jdk \
	python \
	libnss3 \
	curl

COPY download.sh /home/
RUN sh /home/download.sh

ENV PATH /opt/apache-spark/bin:$PATH
ENV MAVEN_HOME /opt/apache-maven-3.3.9


