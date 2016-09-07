# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER Arjun Arkal Rao <aarao@ucsc.edu>

# Copy the test script into the image
COPY test_script.sh /usr/local/bin/test_script.sh

WORKDIR /data
ENTRYPOINT ["sh", "/usr/local/bin/test_script.sh"]
