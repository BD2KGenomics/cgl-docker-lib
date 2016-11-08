FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update; apt-get install -y wget bzip2 perl

# pull down bwa-kit
RUN wget http://sourceforge.net/projects/bio-bwa/files/bwakit/bwakit-0.7.12_x64-linux.tar.bz2

RUN tar -jxvf bwakit-0.7.12_x64-linux.tar.bz2 -C /opt/

RUN rm /opt/bwa.kit/run-bwamem; wget -O /opt/bwa.kit/run-bwamem https://raw.githubusercontent.com/BD2KGenomics/bwa/master/bwakit/run-bwamem; chown 500:500 /opt/bwa.kit/run-bwamem; chmod +x /opt/bwa.kit/run-bwamem

# add wrapper script
ADD wrapper.sh /opt/wrapper.sh

# set entrypoint to bwakit
ENTRYPOINT ["/opt/wrapper.sh"]
