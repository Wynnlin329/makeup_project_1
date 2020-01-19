#!/bin/bash

# N is the node number of hadoop cluster
N=$1

if [ $# = 0 ]
then
	echo "Please specify the node number of hadoop cluster!"
	exit 1
fi

# change slavers file
i=1
rm config/slaves
while [ $i -lt $N ]
do
	echo "slaver$i" >> config/slaves
	((i++))
done 

echo ""

echo -e "\nbuild docker hadoop image\n"

# rebuild hadoop image
sudo docker rmi -f orozcohsu/hadoop:v1
sudo docker build -t orozcohsu/hadoop:v1 .

echo ""
