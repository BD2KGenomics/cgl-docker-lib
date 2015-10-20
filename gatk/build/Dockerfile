FROM java:8-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
	git \
	maven \
	default-jdk

# Create a new source directory
WORKDIR /home

# Get GATK source
RUN git clone https://github.com/broadgsa/gatk-protected
WORKDIR /home/gatk-protected

# Build GATK
RUN mvn -Ddisable.queue install

# Move jar to current WORKDIR
RUN mv /home/gatk-protected/target/GenomeAnalysisTK.jar /home/gatk-protected/gatk.jar
