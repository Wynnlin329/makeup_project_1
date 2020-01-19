#!/bin/bash

echo "starting to delete hadoop volumes"
sudo docker volume rm name-hdfs &> /dev/null
sudo docker volume rm data-hdfs1 &> /dev/null
sudo docker volume rm data-hdfs2 &> /dev/null

echo "finished..."
