FROM quay.io/ucsc_cgl/adam:962-ehf--be13567d00cd4c586edf8ae47d991815c8c72a49

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y \
	python-dev \
	python-pip \
	libnss3 \
	git \
	curl \
	wget \
	apt-transport-https \
	ca-certificates

# Install Toil
RUN pip install toil==3.3.0

# Install adam pipeline
RUN git clone https://github.com/fnothaft/toil-scripts /opt/adam-pipeline
RUN cd /opt/adam-pipeline && git checkout issues/210-adam-local

# Install adam-pipeline's pip dependencies
RUN cd /opt/adam-pipeline && make develop

COPY wrapper.py /opt/adam-pipeline/
COPY README.md /opt/adam-pipeline/

ENTRYPOINT ["/bin/bash", "-c"]
CMD [ "python /opt/adam-pipeline/wrapper.py --help"]
