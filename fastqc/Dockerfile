FROM java:8-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install unzip

RUN wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip -P /opt
RUN unzip /opt/fastqc_v0.11.5.zip -d /opt
RUN chmod +x /opt/FastQC/fastqc

ADD wrapper.sh /opt/FastQC/

RUN mkdir /data
WORKDIR /data
ENTRYPOINT ["/opt/FastQC/wrapper.sh"]
CMD ["--help"]
