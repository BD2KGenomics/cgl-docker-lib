#!/bin/bash

mkdir /mnt/ephemeral/spark

/opt/apache-spark/sbin/start-master.sh

tail -f /opt/apache-spark/logs/* 1>&2
