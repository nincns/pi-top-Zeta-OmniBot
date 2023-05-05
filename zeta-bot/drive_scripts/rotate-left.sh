#!/bin/bash

rpm=35
target_rotation=0.67

direction_fl="CCW"
direction_bl="CCW"
direction_br="CCW"
direction_fr="CCW"

set_directions=()

if [[ ! -z "$direction_fl" ]]; then
  set_directions+=("direction_fl: $direction_fl")
fi

if [[ ! -z "$direction_bl" ]]; then
  set_directions+=("direction_bl: $direction_bl")
fi

if [[ ! -z "$direction_br" ]]; then
  set_directions+=("direction_br: $direction_br")
fi

if [[ ! -z "$direction_fr" ]]; then
  set_directions+=("direction_fr: $direction_fr")
fi

output_file="./messages/bot_rotate_$(date +%F_%H-%M).yaml"

{
  echo "rpm: $rpm"
  echo "target_rotation: $target_rotation"
  for direction in "${set_directions[@]}"; do
    echo "$direction"
  done
} > "$output_file"
