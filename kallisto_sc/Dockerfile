FROM quay.io/ucsc_cgl/kallisto:0.43.0--276c5998c2c7f5b6d5e100e6aba914b53d5425ce
MAINTAINER Trevor Pesout, tpesout@ucsc.edu

# get python libs (and their dependencies)
RUN apt-get -y update
RUN apt-get -y install pkg-config libpng-dev libjpeg8-dev libfreetype6-dev  python-tk libblas-dev liblapack-dev libatlas-base-dev gfortran
RUN pip install numpy matplotlib scipy scikit-learn==0.16.1

# checkout only the source folder of the patcherlab repo
WORKDIR /opt
RUN git clone --no-checkout https://github.com/pachterlab/scRNA-Seq-TCC-prep.git single_cell
WORKDIR /opt/single_cell
RUN git config core.sparseCheckout true
RUN echo "source/*" > .git/info/sparse-checkout
RUN git checkout 0469873bdadcc48e34782882dbd24c3939c0542a

# setup entrypoint
COPY wrapper.sh /opt/single_cell/
ENTRYPOINT ["sh", "/opt/single_cell/wrapper.sh"]
