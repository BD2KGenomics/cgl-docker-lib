mirror=$(python -c "from urllib2 import urlopen; import json; print json.load( urlopen('http://www.apache.org/dyn/closer.lua?path=$path&asjson=1'))['preferred']")

mkdir /opt/apache-spark && \
  curl ${mirror}spark/spark-1.6.3/spark-1.6.3-bin-hadoop2.6.tgz \
  | tar --strip-components=1 -xzC /opt/apache-spark
