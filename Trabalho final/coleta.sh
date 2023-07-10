#!/bin/bash

if [ $# -eq 0 ]
then
    echo "you to inform the source port number"
    exit 1
fi
PORT=$1
while(true)
do
    ss -i '( sport = '$PORT' or dport = '$PORT' )' 
    sleep 1
done