FROM ubuntu:12.04

# install necessary dependencies
RUN apt-get update && \
    apt-get install -y python-dev \
            gcc \
            make \
            libcurl4-openssl-dev \
            python-virtualenv

# create virtualenv and install s3am
RUN virtualenv /opt/s3am --never-download
RUN /opt/s3am/bin/pip install s3am==2.0

ENTRYPOINT ["/opt/s3am/bin/s3am"]
