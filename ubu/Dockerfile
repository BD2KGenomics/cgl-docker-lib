FROM java:8-jdk

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get -y update && apt-get -y install wget

RUN mkdir /opt/ubu
COPY wrapper.sh /opt/ubu/

RUN wget https://github.com/downloads/mozack/ubu/ubu-1.2-jar-with-dependencies.jar -O ubu.jar
RUN mv ubu.jar /opt/ubu/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/ubu/wrapper.sh"]

