#!/bin/bash

# Erzeugen der YAML-Datei
echo "direction_bl: CW" > bot_rotate_$(date +%F_%H-%M).yaml
echo "direction_br: CW" >> bot_rotate_$(date +%F_%H-%M).yaml
echo "direction_fl: CW" >> bot_rotate_$(date +%F_%H-%M).yaml
echo "direction_fr: CW" >> bot_rotate_$(date +%F_%H-%M).yaml
echo "rpm: 35" >> bot_rotate_$(date +%F_%H-%M).yaml
echo "target_rotation: 5.0" >> bot_rotate_$(date +%F_%H-%M).yaml

# Ausgabe der erstellten Datei
echo "Neue Datei erstellt: bot_rotate_$(date +%F_%H-%M).yaml"
