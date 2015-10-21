FROM java:8-jdk

RUN apt-get update && apt-get install -y unzip wget

WORKDIR /opt
RUN wget http://sourceforge.net/projects/snpeff/files/snpEff_latest_core.zip
RUN unzip snpEff_latest_core.zip
RUN rm snpEff_latest_core.zip

RUN mv snpEff snpeff
COPY wrapper.sh /opt/snpeff/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/snpeff/wrapper.sh"]
