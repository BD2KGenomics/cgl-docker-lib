# Run this container as follows
# docker run -v $(pwd):/data jvivian/gencode_hugo_mapping -g <GENE FILES> -i <ISOFORM FILES>

FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN sudo apt-get update && sudo apt-get install -y python-dev python-pip
RUN sudo pip install pandas

RUN mkdir /opt/mapping
RUN mkdir /data

COPY attrs.tsv /opt/mapping/
COPY gencode_hugo_map.py /opt/mapping/

WORKDIR /data

ENTRYPOINT ["python", "/opt/mapping/gencode_hugo_map.py"]
