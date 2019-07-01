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

RUN apt-get update && apt-get install -y \
  unzip \
  npm \
  nodejs

# build mango
WORKDIR /home/mango
RUN /opt/apache-maven-3.3.9/bin/mvn clean package -DskipTests
RUN ls /home/mango/mango-cli/src/main/webapp/resources

# where is node_modules?
RUN mkdir /home/mango/mango-assembly/target/test
WORKDIR /home/mango/mango-assembly/target
RUN unzip mango-assembly-0.0.3-SNAPSHOT.jar -d /home/mango/mango-assembly/target/test
RUN ls test/resources/node_modules/pileup

# remove git libraries to avoid permission errors when copying
RUN rm -rf /home/mango/.git

WORKDIR /home/mango
