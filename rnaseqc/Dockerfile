FROM java:8-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

RUN mkdir /opt/rnaseqc
RUN mkdir /data

ADD wrapper.sh /opt/rnaseqc/

WORKDIR /opt/rnaseqc
RUN wget http://www.broadinstitute.org/cancer/cga/tools/rnaseqc/RNA-SeQC_v1.1.8.jar

WORKDIR /data
ENTRYPOINT ["/opt/rnaseqc/wrapper.sh"]