#!/usr/bin/env bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SPARK_CONNECT_PROTO="https://raw.githubusercontent.com/apache/spark/master/connector/connect/common/src/main/protobuf/spark/connect"

mkdir -p "$DIR"/proto/spark/connect

for FILE in base.proto catalog.proto commands.proto common.proto expressions.proto relations.proto types.proto
do
    curl $SPARK_CONNECT_PROTO/$FILE -o $DIR/proto/spark/connect/$FILE
done