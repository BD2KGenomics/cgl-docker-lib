FROM quay.io/ucsc_cgl/apache-hadoop-common

###
# Much of this is lifted from
# https://github.com/sequenceiq/hadoop-docker/tree/2.6.0/ and
# https://github.com/lresende/docker-yarn-cluster/ with modifications that are
# appropriate for our use case.
###
MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# add script to start hadoop daemons
ADD start-master.sh .

# expose namenode ports
EXPOSE 8020 8022 50070

ENTRYPOINT ["bash", "+x", "start-master.sh"]
