FROM java:8-jdk

MAINTAINER John Vivian, jtvivian@gmail.com

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/picard-tools

RUN wget -O /opt/picard-tools/picard.jar --no-check-certificate https://github.com/broadinstitute/picard/releases/download/2.10.9/picard.jar
COPY wrapper.sh /opt/picard-tools/

WORKDIR /data

ENTRYPOINT ["sh", "/opt/picard-tools/wrapper.sh"]
CMD ["--help"]
