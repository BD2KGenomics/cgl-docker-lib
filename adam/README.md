This directory contains the docker images for
[ADAM](https://www.github.com/bigdatagenomics/adam). These containers build
the ADAM codebase from HEAD, and then run the adam-submit scripts that submit
the code/command to a running Spark cluster.

When the runtime container is run, a port should be opened for the ADAM driver
to communicate with the [Spark master](../apache-spark-master/README.md). The
number of this port should be passed to ADAM as the Spark option
`--conf spark.driver.port <portnumber>`.