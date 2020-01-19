#!/bin/bash

set -e

docker build -f dockerfile_base -t wynnlin/spark-base2.4.4 .
docker build -f dockerfile-spark-master -t spark-master:2.4.4 .
docker build -f dockerfile-spark-worker -t spark-worker:2.4.4 .

