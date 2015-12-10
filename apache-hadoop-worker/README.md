What is this container?
===

This container builds a worker node for Hadoop 2.6.2 HDFS. This runs one service:

* A Datanode: This is an HDFS node where data is stored.

This container inherits from the computationalgenomicslab/apache-hadoop-common:2.6.2 container.

How to run
===

You can run this container with the command:

```
docker run \
  -p 50010:50010 \
  -p 50020:50020 \
  -p 50075:50075 \
  -p 50475:50475 \
  --net=host \
  computationalgenomicslab/apache-hadoop-worker:2.6.2 \
  <master_ip>
```

The [master node](../apache-hadoop-master/README.md) must be started before
this node. The master node IP must be passed to the worker.