This image is for Tachyon's 0.7.1 release. This image is built for the master
node. The difference between this image and the [worker
images](../tachyon-worker/README.md) is strictly the command that is run on
startup. When the master is started, you should pass the node IP address
as an argument.

The following ports should be opened:

* 19998: This is the port the master communicates on.
* 19999: This is the master web UI.