This image is for Apache Spark's 1.5.0 stable release. This image is built for
the master node. The difference between this image and the [worker
images](../apache-spark-worker/README.md) is strictly the command that is run
on startup. This image calls the command to start a Spark standalone master,
which returns an IP address, and takes no arguments.

The following ports should be opened:

* 7077: This is the port that the master listens for worker registration on.
* 8080: This is the port the UI binds to.
* 4040: This is the port that the job UI binds to.
