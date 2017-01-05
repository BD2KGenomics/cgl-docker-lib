FROM ubuntu

ADD rsem_postprocess.sh /
ADD quartile_norm.pl /

RUN mkdir /opt/cgl-docker-lib
RUN mv rsem_postprocess.sh /opt/cgl-docker-lib
RUN mv quartile_norm.pl /opt/cgl-docker-lib

RUN chmod u+x /opt/cgl-docker-lib/rsem_postprocess.sh
RUN chmod u+x /opt/cgl-docker-lib/quartile_norm.pl

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/cgl-docker-lib/rsem_postprocess.sh"]
