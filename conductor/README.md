This directory contains the docker images for
[Conductor](https://github.com/BD2KGenomics/conductor).

Running
===

An example command is:

```
docker run \
       --net=host \
       -p 9999:9999 \
       computationalgenomicslab/conductor:latest \
       --master spark://<spark_master_ip>:7077 \
       --conf spark.driver.port=9999 -- \
       s3://<s3 bucket>/<s3 path> hdfs://<hdfs ip>:<hdfs port>/<hdfs path> 
```