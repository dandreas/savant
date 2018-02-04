#!/bin/sh
while :
do
    python3 savant.py -s 127.0.0.1 -c default -n savant
    echo "Restarting savant..."
done
