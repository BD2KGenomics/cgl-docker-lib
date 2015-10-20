FROM java:8-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

# Copy over jar and place in /opt/cgl-docker-lib
RUN mkdir /opt/gatk
COPY gatk.jar  /opt/gatk/
COPY wrapper.sh /opt/gatk/

# Set WORKDIR to /data -- predefined mount location.
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/gatk/wrapper.sh"]
CMD ["-h"]