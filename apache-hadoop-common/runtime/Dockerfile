FROM ubuntu

###
# Much of this is lifted from
# https://github.com/sequenceiq/hadoop-docker/tree/2.6.0/ and
# https://github.com/lresende/docker-yarn-cluster/ with modifications that are
# appropriate for our use case.
###
MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && \
  apt-get install -y \
    python \
    libnss3 \
    openjdk-8-jre-headless \
    openssh-server \
    openssh-client

# set java path
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre/
ENV PATH $PATH:$JAVA_HOME/bin

# passwordless ssh
#RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
#RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
#RUN ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
#RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# pull down hadoop common jar
RUN mkdir /opt/apache-hadoop
COPY apache-hadoop /opt/apache-hadoop

# set up hadoop environment
ENV HADOOP_PREFIX /opt/apache-hadoop
ENV HADOOP_COMMON_HOME $HADOOP_PREFIX
ENV HADOOP_HDFS_HOME $HADOOP_PREFIX
ENV HADOOP_MAPRED_HOME $HADOOP_PREFIX
ENV HADOOP_YARN_HOME $HADOOP_PREFIX
ENV HADOOP_CONF_DIR $HADOOP_PREFIX/etc/hadoop
ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop

# rewrite some envars in the hadoop-env script
RUN sed -i '/^export JAVA_HOME/ s:.*:export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/\nexport HADOOP_PREFIX=/opt/apache-hadoop\nexport HADOOP_HOME=/opt/apache-hadoop\n:' $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh
RUN sed -i '/^export HADOOP_CONF_DIR/ s:.*:export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop/:' $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh
RUN rm -f $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh.bak
RUN chmod +x $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

# add conf files
ADD hadoop-docker/core-site.xml.template $HADOOP_PREFIX/etc/hadoop/core-site.xml.template
RUN sed -i s/9000/8020/ $HADOOP_PREFIX/etc/hadoop/core-site.xml.template 
ADD hdfs-site.xml $HADOOP_PREFIX/etc/hadoop/hdfs-site.xml
ADD hadoop-docker/mapred-site.xml $HADOOP_PREFIX/etc/hadoop/mapred-site.xml
ADD hadoop-docker/yarn-site.xml $HADOOP_PREFIX/etc/hadoop/yarn-site.xml.template
ADD hadoop-docker/ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/config
RUN chown root:root /root/.ssh/config
