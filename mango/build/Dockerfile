FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Alyssa Morrow, akmorrow@berkeley.edu

# Make port 8080 available for mango browser
EXPOSE 8080
# Make port 8888 available for mango notebook
EXPOSE 8888

WORKDIR /home

# clone mango
RUN git clone https://github.com/bigdatagenomics/mango.git
ENV MAVEN_OPTS "-Xmx2g"

# install curl to get nodejs script
RUN apt-get update && apt-get install -y curl

# get nodejs v6.X
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -

RUN apt-get install -y nodejs

# build mango
WORKDIR /home/mango
RUN git checkout c85b5d2178dbf7ec84cee20c56c57493524d510e # 0.0.3-SNAPSHOT
RUN /opt/apache-maven-3.3.9/bin/mvn clean package -DskipTests

# remove git libraries to avoid permission errors when copying
RUN rm -rf /home/mango/.git

WORKDIR /home/mango
