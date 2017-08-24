FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone gatk4
RUN git clone https://github.com/broadinstitute/gatk.git

# build gatk4
WORKDIR /home/gatk
RUN git checkout c655fef1221615af753bd37590da2c7550ae72b0

RUN ./gradlew bundle
