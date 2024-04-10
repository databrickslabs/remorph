#!/usr/bin/env bash

set -xv

mkdir -p $HOME/spark
cd $HOME/spark

hatch shell

version=$(wget -O - https://dlcdn.apache.org/spark/ | grep 'href="spark' | sed 's:</a>:\n:g' | sed -n 's/.*>//p' | tr -d spark- | tr -d / | sort -r --version-sort | head -1)
spark=spark-${version}-bin-hadoop3
spark_connect=spark-connect_2.12

wget https://dlcdn.apache.org/spark/spark-${version}/${spark}.tgz

tar -xvf ${spark}.tgz

$HOME/spark/${spark}/sbin/start-connect-server.sh --packages org.apache.spark:${spark_connect}:${version}

#sleep time to start the server
sleep 2m

cat $HOME/spark/spark-${version}-bin-hadoop3/logs/spark-runner-org.apache.spark.sql.connect.service.SparkConnectServer*.out