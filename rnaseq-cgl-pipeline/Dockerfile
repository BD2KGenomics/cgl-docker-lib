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
RUN pip install toil

# Install refactored rnaseq pipeline
RUN git clone -b issues/221-refactor-rnaseq-pipeline https://github.com/BD2KGenomics/toil-scripts \
    /opt/rnaseq-pipeline

COPY wrapper.py /opt/rnaseq-pipeline/
COPY README.md /opt/rnaseq-pipeline/

ENTRYPOINT ["python", "/opt/rnaseq-pipeline/wrapper.py"]
CMD ["--help"]
