FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y \
	git \
	wget \
	openjdk-7-jdk \
	python \
	libnss3 \
	curl

RUN mkdir /opt/apache-spark && \
  curl http://apache.osuosl.org/spark/spark-1.5.0/spark-1.5.0-bin-hadoop2.6.tgz \
  | tar --strip-components=1 -xzC /opt/apache-spark

ENV PATH /opt/apache-spark/bin:$PATH

WORKDIR /home

# adam requires maven > 3.1.1, so we can't use the apt-get version (which is 3.0.5)
RUN wget http://apache.mirrorcatalogs.com/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz
RUN tar xzvf apache-maven-3.3.3-bin.tar.gz

# clone adam
RUN git clone https://github.com/bigdatagenomics/adam.git

# build adam
WORKDIR /home/adam
RUN /home/apache-maven-3.3.3/bin/mvn package -DskipTests



