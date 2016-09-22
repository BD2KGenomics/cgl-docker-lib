FROM ubuntu

MAINTAINER Audrey Musselman-Brown almussel@ucsc.edu

RUN apt-get update && \
  apt-get install -y \
    python \
    libnss3 \
    openjdk-8-jdk \
    curl \
    patch

COPY download.sh /home/
RUN sh /home/download.sh

WORKDIR /opt/apache-spark
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre" >> /opt/apache-spark/conf/spark-env.sh

RUN ./make-distribution.sh --name custom-spark --tgz -Phadoop-2.6 -Djoda.time=2.9.4

