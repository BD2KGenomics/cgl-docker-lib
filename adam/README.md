This directory contains the docker images for
[ADAM](https://www.github.com/bigdatagenomics/adam). These containers build
the ADAM codebase from HEAD, and then run the adam-submit scripts that submit
the code/command to a running Spark cluster.

Running
===

When the runtime container is run, a port should be opened for the ADAM driver
to communicate with the [Spark master](../apache-spark-master/README.md). The
number of this port should be passed to ADAM as the Spark option
`--conf spark.driver.port <portnumber>`.

An example command is:

```
docker run \
       --net=host \
       -p 9999:9999 \
       quay.io/ucsc_cgl/adam:latest \
       --master spark://<spark_master_ip>:7077 \
       --conf spark.driver.port=9999 -- \
       flagstat hdfs://<hdfs_master_ip>:8020/mouse_chrM.bam 
```

