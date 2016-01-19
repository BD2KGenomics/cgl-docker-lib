What is this container?
===

This container builds the "master" node for Hadoop 2.6.2 HDFS:

* The Namenode: This is the node that controls HDFS.

This container inherits from the quay.io/ucsc_cgl/apache-hadoop-common:2.6.2 container.

How to run
===

You can run this container with the command:

```
docker run \
  -p 8020:8020 \
  -p 8022:8022 \
  -p 50070:50070 \
  --net=host \
  quay.io/ucsc_cgl/apache-hadoop-master:2.6.2 \
  <master_ip>
```

Testing the container out
===

When the container boots, you can check to see if the container is up by looking
at the HDFS web interface at `http://<master_ip>:50070`.

Once you've got at least one datanode connected, you can put files in HDFS. You
can get a terminal on the Namenode by running:

```
docker exec -it <image name/id> /bin/bash
```

Once you've got this terminal, you can add a simple test file to HDFS by
running:

```
root@dev:/# wget cs.berkeley.edu/~massie/bams/mouse_chrM.bam
root@dev:/# ${HADOOP_HDFS_HOME}/bin/hdfs dfs -put mouse_chrM.bam /mouse_chrM.bam
root@dev:/# ${HADOOP_HDFS_HOME}/bin/hdfs dfs -ls /mouse_chrM.bam
```

This file should be visible from the web UI at
`http://<master_ip>:50070/explorer.html#/`.
