This directory contains the docker images for
[Mango](https://www.github.com/bigdatagenomics/mango). These containers build
the mango codebase from HEAD, and then run the mango-submit scripts that submit
the code/command to a running Spark cluster.

Running
===

When the runtime container is run, a port should be opened for the Mango driver
to communicate with the [Spark master](../apache-spark-master/README.md). The
number of this port should be passed to mango as the Spark option
`--conf spark.driver.port <portnumber>`.

An example command to run mango browser is:

```
docker run \
       --net=host \
       -p 8080:8080 \
       quay.io/ucsc_cgl/mango:latest \
       --master spark://<spark_master_ip>:7077 \
       --conf spark.driver.port=9999 -- \
       hdfs://<hdfs_master_ip>:8020/hg19.fa -reads hdfs://<hdfs_master_ip>:8020/mouse_chrM.bam
```

An example command to run mango notebook is:

```
docker run \
       --net=host \
       --entrypoint=/opt/cgl-docker-lib/mango/bin/mango-notebook \
       -p 8888:8888 \
       quay.io/ucsc_cgl/mango:latest -- --ip=0.0.0.0 --allow-root \
       --master spark://<spark_master_ip>:7077 \
       --conf spark.driver.port=9999
```
