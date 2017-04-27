FROM quay.io/ucsc_cgl/apache-spark-common:1.6.3--f21484f0191eb362b07170211124413cb28c17f7

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# add master runner script
ADD run-master.sh .

ENTRYPOINT ["bash", "+x", "run-master.sh"]
