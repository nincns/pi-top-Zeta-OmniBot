#!/bin/bash

source ./speed.conf

rpm=$((rpm - 10))

if (( $rpm < -114 )); then
  rpm=-114
fi

echo "rpm=$rpm" > ./speed.conf
