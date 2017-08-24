FROM ubuntu:14.04

RUN apt-get update && \
  apt-get install -y python libnss3 wget unzip libtbb-dev

# Download bowtie2 binary
RUN mkdir /opt/bowtie2
WORKDIR /opt/bowtie2
RUN wget https://github.com/BenLangmead/bowtie2/releases/download/v2.3.2/bowtie2-2.3.2-linux-x86_64.zip
RUN unzip bowtie2-2.3.2-linux-x86_64.zip

ENTRYPOINT ["/opt/bowtie2/bowtie2-2.3.2/bowtie2"]