FROM ubuntu

RUN apt-get update && apt-get install -y python

RUN mkdir /opt/cgl-docker-lib
RUN mkdir /MapSplice-v2.1.8
ADD MapSplice-v2.1.8 /MapSplice-v2.1.8
RUN mv MapSplice-v2.1.8/ /opt/cgl-docker-lib/
ADD wrapper.sh /opt/cgl-docker-lib/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/cgl-docker-lib/wrapper.sh"]