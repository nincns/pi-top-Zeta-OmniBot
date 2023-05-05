#!/bin/bash

source ./speed.conf

echo "distance: 30.0" > ./messages/bot_move_$(date +%F_%H-%M).yaml
echo "rpm: $rpm" >> ./messages/bot_move_$(date +%F_%H-%M).yaml
