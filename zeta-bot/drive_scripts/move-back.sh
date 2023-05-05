#!/bin/bash

source ./speed.conf

if (( $rpm > 0 )); then
  rpm=$(( -1 * rpm ))
fi

cat <<EOF > ./messages/bot_move_$(date +%F_%H-%M).yaml
distance: 20.0
rpm: $rpm
EOF
