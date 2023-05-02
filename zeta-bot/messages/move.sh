#!/bin/bash

# Erzeugen der YAML-Datei
echo "distance: 20.0" > bot_move_$(date +%F_%H-%M).yaml
echo "rpm: 25" >> bot_move_$(date +%F_%H-%M).yaml

# Ausgabe der erstellten Datei
echo "Neue Datei erstellt: bot_move_$(date +%F_%H-%M).yaml"
