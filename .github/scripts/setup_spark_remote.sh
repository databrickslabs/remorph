#!/usr/bin/env bash

set -xv

mkdir -p $HOME/spark
cd $HOME/spark

version=$(wget -O - https://dlcdn.apache.org/spark/ | grep 'href="spark' | grep -v 'preview' | sed 's:</a>:\n:g' | sed -n 's/.*>//p' | tr -d spark- | tr -d / | sort -r --version-sort | head -1)
spark=spark-${version}-bin-hadoop3
spark_connect=spark-connect_2.12

mkdir ${spark}
cd {spark}

SERVER_SCRIPT=$HOME/spark/${spark}/sbin/start-connect-server.sh

## check the spark version already exist ,if not download the respective version
if [ -f ${SERVER_SCRIPT} ];then
  echo "Spark Version already exists"
else
  wget https://dlcdn.apache.org/spark/spark-${version}/${spark}.tgz
  tar -xvf ${spark}.tgz
fi

## check spark remote is running,if not start the spark remote
${SERVER_SCRIPT} --packages org.apache.spark:${spark_connect}:${version} > $HOME/spark/log.out

if [ $? -ne 0 ]; then
    count=$(tail ${HOME}/spark/log.out | grep "SparkConnectServer running as process" | wc -l)
    if [ "${count}" == "0" ]; then
            echo "Failed to start the server"
        exit 1
    fi
    #sleep time to start the server
    sleep 2m
    echo "Server Already Running"
fi
