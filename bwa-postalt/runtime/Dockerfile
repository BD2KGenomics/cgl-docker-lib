FROM ubuntu:12.04

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# make artifact directories
RUN mkdir /opt/bwa-postalt

# add k8
COPY k8 /opt/k8

# add bwa-postalt.js
COPY bwa-postalt.js /opt/bwa-postalt/bwa-postalt.js

# set the entrypoint to invoke k8 and the bwa-postalt.js script
ENTRYPOINT ["/opt/k8/k8", "/opt/bwa-postalt/bwa-postalt.js"]
