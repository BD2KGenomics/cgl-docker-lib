FROM java:8-jdk
MAINTAINER Trevor Pesout, tpesout@ucsc.edu

RUN apt-get update && apt-get install -y tabix

# Copy over jar and place in /opt/cgl-docker-lib
RUN mkdir /opt/rtg_tools
COPY rtg-tools.jar  /opt/rtg_tools/
COPY LICENSE.txt /opt/rtg_tools/
COPY wrapper.sh /opt/rtg_tools/

# Set WORKDIR to /data -- predefined mount location.
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/rtg_tools/wrapper.sh"]
