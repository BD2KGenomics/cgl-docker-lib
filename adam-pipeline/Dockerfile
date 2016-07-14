FROM ubuntu:14.04

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y \
	git \
	openjdk-7-jdk \
	python-dev \
	python-pip \
	libnss3 \
	curl \
	wget \
	apt-transport-https \
	ca-certificates

# Get the 1.9.1 binary
RUN wget https://get.docker.com/builds/Linux/x86_64/docker-1.9.0 -O /usr/local/bin/docker
RUN chmod u+x /usr/local/bin/docker

# Install Toil
RUN pip install toil==3.3.0

# Install adam pipeline
RUN git clone https://github.com/fnothaft/toil-scripts /opt/adam-pipeline
RUN cd /opt/adam-pipeline && git checkout issues/210-adam-local

# Install adam-pipeline's pip dependencies
RUN cd /opt/adam-pipeline && make develop

COPY wrapper.py /opt/adam-pipeline/
COPY README.md /opt/adam-pipeline/

ENTRYPOINT ["python", "/opt/adam-pipeline/wrapper.py"]
CMD ["--help"]
