#!/bin/bash

# the default node number is 3
N=${1:-3}

echo "default 1 master and 2 slavers"

docker volume inspect name-hdfs &> /dev/null
if [ $? -eq 1 ]
then
    echo "create docker volume: name-hdfs"
    sudo docker volume create --name name-hdfs &> /dev/null
fi

# start hadoop master container
sudo docker rm -f master &> /dev/null
echo "start master container..."
sudo docker run -itd \
                --net=hadoop \
                -p 50070:50070 \
                -p 2222:22 \
                -p 8088:8088 \
                -v name-hdfs:/root/hdfs \
                --name master \
                --hostname master \
                wynnlin/hadoop-cluster:v1 &> /dev/null


# start hadoop slaver container
i=1
while [ $i -lt $N ]
do
        docker volume inspect data-hdfs$i &> /dev/null
        if [ $? -eq 1 ] 
        then
            echo "create docker volume: data-hdfs$i"
            sudo docker volume create --name data-hdfs$i &> /dev/null
        fi
	sudo docker rm -f slaver$i &> /dev/null
	echo "start slaver$i container..."
	sudo docker run -itd \
                        -v data-hdfs$i:/root/hdfs \
	                --net=hadoop \
	                --name slaver$i \
	                --hostname slaver$i \
	                wynnlin/hadoop-cluster:v1 &> /dev/null
	i=$(( $i + 1 ))
done 

# get into hadoop master container
sudo docker exec -it master bash
