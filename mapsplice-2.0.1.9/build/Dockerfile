FROM ubuntu:12.04

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update && apt-get install -y \
	wget \
	make \
	g++ \
	unzip \
	zlib1g-dev \
	libncurses5-dev \
	python

RUN wget --no-check-certificate https://webshare.bioinf.unc.edu/public/mRNAseq_TCGA/MapSplice_multithreads_2.0.1.9.tar.gz

RUN tar -xvf MapSplice_multithreads_2.0.1.9.tar.gz

WORKDIR MapSplice_multi_threads_2.0.1.9

RUN make

WORKDIR /


