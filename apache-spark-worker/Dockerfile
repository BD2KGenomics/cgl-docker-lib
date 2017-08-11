FROM quay.io/ucsc_cgl/apache-spark-common:1.6.3--f21484f0191eb362b07170211124413cb28c17f7

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# set spark worker port
ENV SPARK_WORKER_PORT 7075

# add worker runner
ADD run-worker.sh .

ENTRYPOINT ["bash", "-x", "run-worker.sh"]
