#!/bin/bash
./network.sh up -i 2.1

echo "Sleep for 30 seconds"
sleep 30

./network.sh createChannel

echo "Sleep for 15 seconds"
sleep 15

./network.sh deployCC -d 20

echo "Sleep for 10 seconds"
sleep 10

./interact.sh