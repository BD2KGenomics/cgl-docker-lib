FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER John Vivian <jtvivian@gmail.com>

RUN apt-get update && apt-get install -y \
    git \
    python-dev \
    python-pip \
    wget \
    curl \
    apt-transport-https \
    ca-certificates

# Get the 1.9.1 binary
RUN wget https://get.docker.com/builds/Linux/x86_64/docker-1.9.1 -O /usr/local/bin/docker
RUN chmod u+x /usr/local/bin/docker

# Install Toil
RUN pip install toil==3.3.0

# Install refactored rnaseq pipeline
RUN git clone https://github.com/BD2KGenomics/toil-scripts /opt/rnaseq-pipeline
RUN cd /opt/rnaseq-pipeline && git reset --hard 77510fb075f5865050621968e2dc6b2ac8cf7c87

COPY wrapper.py /opt/rnaseq-pipeline/
COPY README.md /opt/rnaseq-pipeline/

ENTRYPOINT ["python", "/opt/rnaseq-pipeline/wrapper.py"]
CMD ["--help"]
