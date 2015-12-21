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



