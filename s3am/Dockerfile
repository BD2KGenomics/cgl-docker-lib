FROM ubuntu:12.04

MAINTAINER Frank Austin Nothaft

# install necessary dependencies
RUN apt-get update && \
    apt-get install -y python-dev \
            gcc \
            make \
            libcurl4-openssl-dev \
            python-virtualenv

# create virtualenv and install s3am
RUN virtualenv /opt/s3am && . /opt/s3am/bin/activate
RUN pip install s3am

# add wrapper script
WORKDIR /opt/
ADD wrapper.sh /opt/wrapper.sh

ENTRYPOINT ["bash", "+x", "/opt/wrapper.sh"]