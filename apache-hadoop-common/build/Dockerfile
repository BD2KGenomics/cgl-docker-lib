FROM ubuntu

###
# Much of this is lifted from
# https://github.com/sequenceiq/hadoop-docker/tree/2.6.0/, with modifications
# that are appropriate for our use case.
###
MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && \
  apt-get install -y \
    python \
    curl \
    git

# pull down hadoop common jar
RUN mkdir /opt/apache-hadoop && \
  curl http://apache.osuosl.org/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz \
  | tar --strip-components=1 -xzC /opt/apache-hadoop
RUN chmod -R ugoa+rw /opt/apache-hadoop/share/hadoop/*/tomcat
RUN chmod -R ugoa+r /opt/apache-hadoop
RUN rm -rf /opt/apache-hadoop/src/

# check out sequenceiq/hadoop-docker repo
WORKDIR /opt/
RUN git clone https://github.com/sequenceiq/hadoop-docker.git
RUN cd hadoop-docker && \
  git checkout 2.6.0
