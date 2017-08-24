FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && \
  apt-get install -y \
    python \
    libnss3 \
    openjdk-8-jre-headless \
    curl

# Install statically linked version of docker client
RUN curl https://get.docker.com/builds/Linux/x86_64/docker-1.12.3.tgz \
    | tar -xvzf - --transform='s,[^/]*/,,g' -C /usr/local/bin/ \
    && chmod u+x /usr/local/bin/docker

# pull down spark jar
RUN mkdir /opt/apache-spark && \
  curl http://apache.osuosl.org/spark/spark-2.1.1/spark-2.1.1-bin-hadoop2.6.tgz \
  | tar --strip-components=1 -xzC /opt/apache-spark

# add spark to path
ENV PATH /opt/apache-spark/bin:$PATH

# add master runner script
ADD run-master.sh .

ENTRYPOINT ["bash", "+x", "run-master.sh"]
