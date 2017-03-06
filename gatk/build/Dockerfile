FROM java:8-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
    wget \
	maven \
	default-jdk

# Create a new source directory
WORKDIR /home

# Get GATK source
WORKDIR /home/gatk-protected
RUN wget --no-check-certificate https://github.com/broadgsa/gatk-protected/archive/3.7.zip \
    && unzip 3.7.zip \
    && rm 3.7.zip
WORKDIR /home/gatk-protected/gatk-protected-3.7

# Ça me rend fou!
# which roughly translates to "I can't even...!"
#
# See http://gatkforums.broadinstitute.org/wdl/discussion/6533/compiling-gatk-3-5
RUN find . -name "*.java" -exec sed -i -e "s/import oracle.jrockit.jfr/\/\/import oracle.jrockit.jfr/g" {} \;

# Build GATK
RUN mvn -Ddisable.queue install

# Move jar to currently mounted directory (file is used in the runtime image)
RUN mv /home/gatk-protected/gatk-protected-3.7/target/GenomeAnalysisTK.jar /home/gatk-protected/gatk.jar
