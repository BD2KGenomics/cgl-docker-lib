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

# Check out the 3.5 tag
RUN git checkout 3.5

# Ça me rend fou!
# which roughly translates to "I can't even...!"
#
# See http://gatkforums.broadinstitute.org/wdl/discussion/6533/compiling-gatk-3-5
RUN find . -name "*.java" -exec sed -i -e "s/import oracle.jrockit.jfr/\/\/import oracle.jrockit.jfr/g" {} \;

# Build GATK
RUN mvn -Ddisable.queue install

# Move jar to current WORKDIR
RUN mv /home/gatk-protected/target/GenomeAnalysisTK.jar /home/gatk-protected/gatk.jar
