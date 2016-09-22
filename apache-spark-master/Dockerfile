FROM quay.io/ucsc_cgl/apache-spark-common:1.5.2

MAINTAINER Audrey Musselman-Brown, almussel@ucsc.edu

# add master runner script
ADD run-master.sh .

ENTRYPOINT ["bash", "+x", "run-master.sh"]
