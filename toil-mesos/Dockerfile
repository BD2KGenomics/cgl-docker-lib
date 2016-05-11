FROM mesosphere/mesos:0.25.1

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

# Install toil-scripts
RUN pip install toil-scripts

# Install mesos.native
RUN wget http://downloads.mesosphere.io/master/ubuntu/14.04/mesos-0.25.1-py2.7-linux-x86_64.egg
RUN easy_install -a *.egg

# Create toil-mesos dir and copy in wrapper
RUN mkdir /opt/toil-mesos
COPY wrapper.sh /opt/toil-mesos/

ENTRYPOINT ["/opt/toil-mesos/wrapper.sh"]
CMD ["--help"]
