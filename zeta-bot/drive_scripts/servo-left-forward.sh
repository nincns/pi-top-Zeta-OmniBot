#!/bin/bash

# Pfad zur temporären Textdatei
temp_file="S0.txt"
yaml_output_dir="messages"

# Überprüfen, ob die temporäre Textdatei existiert und den Winkel initialisieren
if [ -e "$temp_file" ]; then
    current_angle=$(cat "$temp_file")
else
    current_angle=0
fi

# Winkel aktualisieren und in der temporären Textdatei speichern
new_angle=$((current_angle - 10))
echo "$new_angle" > "$temp_file"

# YAML-Datei erstellen
timestamp=$(date +"%Y-%m-%d_%H-%M")
counter=1

while true; do
    yaml_filename="msg_bot_servo_${timestamp}_${counter}.yaml"
    yaml_filepath="${yaml_output_dir}/${yaml_filename}"
    
    if [ ! -e "$yaml_filepath" ]; then
        break
    fi
    counter=$((counter + 1))
done

# YAML-Datei mit den Servo-Informationen schreiben
cat << EOF > "$yaml_filepath"
angle: $new_angle
servo_name: S0
EOF
