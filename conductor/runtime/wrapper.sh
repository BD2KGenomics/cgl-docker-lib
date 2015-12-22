#! /bin/bash

SPARK_SUBMIT=/opt/cgl-docker-lib/apache-spark/bin/spark-submit
CONDUCTOR_JAR=/opt/cgl-docker-lib/conductor/conductor/target/conductor-0.5-SNAPSHOT-distribution.jar


# Argument splitting code adapted from
# https://github.com/bigdatagenomics/adam/blob/master/bin/adam-submit

for ARG in "$@"; do
  shift
  if [[ $ARG == "--" ]]; then
    DD=True
    POST_DD=( "$@" )
    break
  fi
  PRE_DD+=("$ARG")
done

if [[ $DD == True ]]; then
  SPARK_ARGS="${PRE_DD[@]}"
  CONDUCTOR_ARGS="${POST_DD[@]}"
else
  SPARK_ARGS=()
  CONDUCTOR_ARGS="${PRE_DD[@]}"
fi

$SPARK_SUBMIT $SPARK_ARGS $CONDUCTOR_JAR $CONDUCTOR_ARGS
