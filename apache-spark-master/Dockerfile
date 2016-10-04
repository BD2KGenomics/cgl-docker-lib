FROM quay.io/ucsc_cgl/apache-spark-common:1.5.2--9885dd3736e1c59552e2a821b5a4690a5d23f1ab

MAINTAINER Audrey Musselman-Brown, almussel@ucsc.edu

# add master runner script
ADD run-master.sh .

ENTRYPOINT ["bash", "+x", "run-master.sh"]
