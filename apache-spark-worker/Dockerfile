FROM quay.io/ucsc_cgl/apache-spark-common:1.5.2

MAINTAINER Audrey Musselman-Brown, almussel@ucsc.edu

# set spark worker port
ENV SPARK_WORKER_PORT 7075

# add worker runner
ADD run-worker.sh .

ENTRYPOINT ["bash", "-x", "run-worker.sh"]
