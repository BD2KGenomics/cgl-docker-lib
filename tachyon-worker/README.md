This image is for Tachyon's 0.7.1 release. This image is built for the worker
node. The difference between this image and the [master
images](../tachyon-master/README.md) is strictly the command that is run on
startup. When the instance is started, the master IP address should be passed.
Worker nodes should be started up after the master is started.

The following ports should be opened:

* 29998: This is the port the worker communicates on.
* 29999: This is the worker web UI.