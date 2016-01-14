FROM computationalgenomicslab/spark-and-maven:1.5.2.3.3.3-build

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone adam
RUN git clone https://github.com/bigdatagenomics/adam.git

# build adam
WORKDIR /home/adam
RUN git checkout 49b614d5334871e4ea879290bec650e0ab94edaf
RUN /opt/apache-maven-3.3.3/bin/mvn package -DskipTests
