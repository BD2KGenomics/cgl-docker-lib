FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN mkdir /opt/genetorrent
RUN mkdir /data
COPY wrapper.sh /opt/genetorrent/
# RUN sudo apt-get update && sudo apt-get install -y wget curl libcurl3 libcurl4-openssl-dev
RUN sudo apt-get install -y wget curl libicu52

RUN wget https://cghub.ucsc.edu/software/downloads/GeneTorrent/3.8.7/GeneTorrent-download-3.8.7-207-Ubuntu14.04.x86_64.tar.gz
RUN tar -xvf *.tar.gz
RUN mv cghub /opt/genetorrent/

WORKDIR /data

ENV LD_LIBRARY_PATH /opt/genetorrent/cghub/lib

ENTRYPOINT ["sh", "/opt/genetorrent/wrapper.sh"]