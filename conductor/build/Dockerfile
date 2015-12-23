FROM computationalgenomicslab/spark-and-maven:1.5.2.3.3.3-build

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# clone conductor
WORKDIR /home
RUN git clone https://github.com/BD2KGenomics/conductor.git

# build conductor
WORKDIR /home/conductor
RUN /opt/apache-maven-3.3.3/bin/mvn package \
    -DskipTests \
    -Dhadoop.version=2.6.0 \
    -Dspark.version=1.5.2
