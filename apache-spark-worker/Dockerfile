FROM quay.io/ucsc_cgl/apache-spark-common:1.5.2--9885dd3736e1c59552e2a821b5a4690a5d23f1ab

MAINTAINER Audrey Musselman-Brown, almussel@ucsc.edu

# set spark worker port
ENV SPARK_WORKER_PORT 7075

# add worker runner
ADD run-worker.sh .

ENTRYPOINT ["bash", "-x", "run-worker.sh"]
