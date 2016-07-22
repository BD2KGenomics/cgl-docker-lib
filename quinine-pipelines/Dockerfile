FROM quay.io/ucsc_cgl/quinine

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

# Install quinine pipeline
RUN git clone https://github.com/fnothaft/toil-scripts /opt/toil-scripts
RUN cd /opt/toil-scripts && git checkout issues/380-quinine

# Install the pip dependencies
RUN cd /opt/toil-scripts && make develop

COPY quinine-pipelines.sh /opt/toil-scripts/
COPY README.md /opt/toil-scripts/

ENTRYPOINT ["/bin/bash", "-c"]
CMD [ "/opt/toil-scripts/quinine-pipelines.sh --help"]
