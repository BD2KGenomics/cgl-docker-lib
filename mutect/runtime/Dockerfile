FROM java

MAINTAINER John Vivian, jtvivian@gmail.com

# default-jdk needed to run MuTect/GATK
RUN apt-get update && apt-get install -y default-jdk

# Copy over jar and place in /opt/cgl-docker-lib
RUN mkdir /opt/cgl-docker-lib
ADD mutect-1.1.7.jar  /
RUN cp mutect-1.1.7.jar /opt/cgl-docker-lib

# Set WORKDIR to /data -- predefined mount location.
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["java", "-jar", "/opt/cgl-docker-lib/mutect-1.1.7.jar"]

