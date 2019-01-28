FROM    ubuntu:14.04

MAINTAINER "John Vivian"

LABEL version="1.4.0" \
      mode="gdc-client-1.4.0" \
      description="docker image to run NCI gdc-client"

# Install GDC-Client
RUN    apt-get update
RUN    apt-get install -y wget zip unzip
RUN    cd /opt && wget https://gdc.cancer.gov/system/files/authenticated%20user/0/gdc-client_v1.4.0_Ubuntu_x64.zip && unzip gdc-client_v1.4.0_Ubuntu_x64.zip
RUN    cp /opt/gdc-client /usr/local/bin/

# Data dir
RUN mkdir /data
WORKDIR    /data

# Set ENTRYPOINT
ENTRYPOINT ["/usr/local/bin/gdc-client"]
CMD ["-h"]
