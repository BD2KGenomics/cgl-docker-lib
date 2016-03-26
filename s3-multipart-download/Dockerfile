# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER John Vivian <jtvivian@gmail.com>

# Update the repository sources list
RUN apt-get update && apt-get install --yes \
        git \
        python-pip

RUN git clone https://github.com/jvivian/s3-multipart /opt/s3-multipart
RUN cd /opt/s3-multipart && pip install -r requirements.txt

# CGL Boilerplate
COPY wrapper.sh /opt/s3-multipart
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/s3-multipart/wrapper.sh"]
