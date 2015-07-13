FROM ubuntu
MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update -y && apt-get upgrade -y && apt-get -y install cmake zlib1g-dev libhdf5-dev git build-essential

RUN git clone https://github.com/pachterlab/kallisto.git

WORKDIR kallisto
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN make
RUN make install
WORKDIR src

ENTRYPOINT ["kallisto"]
