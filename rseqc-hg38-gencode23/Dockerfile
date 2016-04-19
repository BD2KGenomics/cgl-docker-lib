FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
            build-essential \
            python-dev \
            R-base \
            samtools \
            python-pip \
            python-numpy

RUN pip install cython

# Install and setup RSeQC
COPY RSeQC-2.6.3.tar.gz /opt/
RUN cd /opt && tar -zxf RSeQC-2.6.3.tar.gz
RUN cd /opt/RSeQC-2.6.3 && python setup.py install

COPY rseqc.sh /opt/RSeQC-2.6.3/
COPY wrapper.sh /opt/RSeQC-2.6.3/
COPY gencode.v23.bed /opt/RSeQC-2.6.3/

RUN mkdir /data
WORKDIR /data
ENTRYPOINT ["/opt/RSeQC-2.6.3/wrapper.sh"]
