FROM java:7-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
	git \
	maven \
	default-jdk

# Create a new source directory
WORKDIR /home
RUN mkdir mutect-src
WORKDIR /home/mutect-src

# Get Mutect source
RUN git clone https://github.com/broadinstitute/mutect

# Get GATK source
RUN git clone https://github.com/broadgsa/gatk-protected
WORKDIR /home/mutect-src/gatk-protected
RUN git reset --hard 3.1

# Build GATK
RUN mvn -Ddisable.queue install

# Build MuTect
WORKDIR /home/mutect-src/mutect
RUN mvn verify

# Move mutect.jar to /home directory
RUN mv target/mutect* /home

# Set working directory and cleanup
WORKDIR /home
RUN rm -rf mutect-src
