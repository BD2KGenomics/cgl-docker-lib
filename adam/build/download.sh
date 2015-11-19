#!/bin/bash

# find mirror
mirror=$(python -c "from urllib2 import urlopen; import json; print json.load( urlopen('http://www.apache.org/dyn/closer.cgi?path=$path&asjson=1'))['preferred']")

# pull down spark
mkdir /opt/apache-spark
curl ${mirror}spark/spark-1.5.0/spark-1.5.0-bin-hadoop2.6.tgz \
  | tar --strip-components=1 -xzC /opt/apache-spark

# we rely on apache maven > 3.1.1 to build ADAM, so we can't use the
# version of maven installed by apt-get
mkdir /opt/apache-maven-3.3.3
curl ${mirror}maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz \
  | tar --strip-components=1 -xzC /opt/apache-maven-3.3.3
