#!/bin/bash

sleep 10

if [ "$SPARK_MODE" = "master" ]; then
  /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master --host spark-master --port 7077 --webui-port 8080
else
  /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker $SPARK_MASTER_URL
fi

spark-submit --master local[*] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 main.py

tail -f /dev/null