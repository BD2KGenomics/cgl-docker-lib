FROM quay.io/ucsc_cgl/adam:962-ehf--be13567d00cd4c586edf8ae47d991815c8c72a49

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# copy jar
COPY quinine /opt/cgl-docker-lib/quinine

ENTRYPOINT ["/opt/cgl-docker-lib/quinine/bin/quinine-submit"]
