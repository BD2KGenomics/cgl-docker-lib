FROM java:8-jdk

MAINTAINER Trevor Pesout, tpesout@ucsc.edu

RUN apt-get update && apt-get install -y \
    git \
	ant \
	unzip

# Create a new source directory
WORKDIR /home

# Get RTG tools
WORKDIR /home/rtg-tools
RUN git clone https://github.com/RealTimeGenomics/rtg-tools.git
WORKDIR /home/rtg-tools/rtg-tools
RUN git checkout 3.8.3

# build
RUN ant zip-nojre

# Move jar to currently mounted directory (file is used in the runtime image)
WORKDIR /home/rtgtools-protected
RUN mv /home/rtg-tools/rtg-tools/build/rtg-tools.jar /home/rtgtools-protected/rtg-tools.jar
RUN mv /home/rtg-tools/rtg-tools/LICENSE.txt /home/rtgtools-protected/LICENSE.txt
