FROM ubuntu:14.04

MAINTAINER John Vivian

RUN sudo apt-get update && sudo apt-get install -y wget

RUN wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.1/sratoolkit.2.8.1-ubuntu64.tar.gz
RUN tar -xvf sratoolkit.2.8.1-ubuntu64.tar.gz
RUN rm sratoolkit.2.8.1-ubuntu64.tar.gz
RUN mkdir /opt/fastq-dump/
RUN sudo mv sratoolkit.2.8.1-ubuntu64 /opt/fastq-dump/

COPY wrapper.sh /opt/fastq-dump/
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/fastq-dump/wrapper.sh"]
CMD ["-h"]