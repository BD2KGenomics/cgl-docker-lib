FROM python:2.7

RUN apt-get update && apt-get install -y --no-install-recommends \
  r-base \
  zlib1g-dev \
  time

RUN pip install RSeQC==2.6.4

RUN wget -qO- https://github.com/lomereiter/sambamba/releases/download/v0.6.7/sambamba_v0.6.7_linux.tar.bz2 \
  | tar xj -C /usr/local/bin

RUN wget -qO- https://github.com/GregoryFaust/samblaster/releases/download/v.0.1.24/samblaster-v.0.1.24.tar.gz \
  | tar xz -C /tmp \
  && cd /tmp/samblaster-v.0.1.24/ && make && mv samblaster /usr/local/bin && rm -rf /tmp/samblaster-v-0.1.24

WORKDIR /ref
RUN wget -qO- http://courtyard.gi.ucsc.edu/~jvivian/bamqc/hg38_GENCODE_v23.bed.gz \
  | gunzip -c > /ref/hg38_GENCODE_v23_basic.bed

#WORKDIR /app
#ADD ./requirements.txt /app/requirements.txt
#RUN pip install --no-cache-dir -r /app/requirements.txt

RUN R -e 'install.packages(c("rjson"), repos="http://cran.us.r-project.org")'

RUN mkdir /app
ADD . /app

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
