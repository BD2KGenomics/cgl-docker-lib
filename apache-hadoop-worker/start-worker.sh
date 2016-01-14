#!/bin/bash

HADOOP_PREFIX=/opt/apache-hadoop
HADOOP_CONF_DIR=${HADOOP_PREFIX}/etc/hadoop
ln -s ${HADOOP_PREFIX} /usr/local/hadoop

# make a directory in the mounted volume
mkdir /ephemeral/hdfs

# overwrite hostname in conf
if [ $# -ne 0 ]; then
    sed "s/HOSTNAME/${1}/g" $HADOOP_PREFIX/etc/hadoop/core-site.xml.template > $HADOOP_PREFIX/etc/hadoop/core-site.xml
    sed -e "s/yarn.nodemanager.aux-services/yarn.resourcemanager.hostname/g" \
        -e "s/mapreduce_shuffle/${1}/g" \
        $HADOOP_PREFIX/etc/hadoop/yarn-site.xml.template > $HADOOP_PREFIX/etc/hadoop/yarn-site.xml
else
    sed "s/HOSTNAME/localhost/g" $HADOOP_PREFIX/etc/hadoop/core-site.xml.template > $HADOOP_PREFIX/etc/hadoop/core-site.xml
    sed -e "s/yarn.nodemanager.aux-services/yarn.resourcemanager.hostname/g" \
        -e "s/mapreduce_shuffle/localhost/g" \
        $HADOOP_PREFIX/etc/hadoop/yarn-site.xml.template > $HADOOP_PREFIX/etc/hadoop/yarn-site.xml
fi

# set up the environment
$HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

# start sshd
service ssh start

# start the datanode daemon
$HADOOP_PREFIX/sbin/hadoop-daemon.sh --config $HADOOP_CONF_DIR --script hdfs start datanode

# follow some logs forever
tail -f /opt/apache-hadoop/logs/*