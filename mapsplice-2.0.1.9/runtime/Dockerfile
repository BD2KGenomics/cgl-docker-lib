FROM ubuntu:12.04

RUN apt-get update && apt-get install -y python

RUN mkdir /opt/mapsplice/
RUN mkdir /MapSplice-v2.0.1.9
ADD MapSplice_multi_threads_2.0.1.9 /MapSplice_multi_threads_2.0.1.9
RUN mv MapSplice_multi_threads_2.0.1.9/ /opt/mapsplice/
ADD wrapper.sh /opt/mapsplice/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/mapsplice/wrapper.sh"]