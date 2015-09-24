FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && \
  apt-get install -y python libnss3 openjdk-7-jre-headless curl

# pull down spark jar
RUN mkdir /opt/apache-spark && \
  curl http://apache.osuosl.org/spark/spark-1.5.0/spark-1.5.0-bin-hadoop2.6.tgz \
  | tar --strip-components=1 -xzC /opt/apache-spark

# add spark to path
ENV PATH /opt/apache-spark/bin:$PATH

# add master runner script
ADD run-master.sh .

ENTRYPOINT ["bash", "+x", "run-master.sh"]
