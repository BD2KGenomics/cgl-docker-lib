FROM java

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get -y update && apt-get -y install wget

RUN mkdir /opt/cgl-docker-lib

RUN wget https://github.com/downloads/mozack/ubu/ubu-1.2-jar-with-dependencies.jar -O ubu.jar
RUN mv ubu.jar /opt/cgl-docker-lib

ENTRYPOINT ["java", "-jar", "/opt/cgl-docker-lib/ubu.jar"]

