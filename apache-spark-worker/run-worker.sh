/opt/apache-spark/sbin/start-slave.sh $1

tail -f /opt/apache-spark/logs/* 1>&2
