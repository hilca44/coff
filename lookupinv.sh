#!/bin/bash
source ./fu.sh
# Verzeichnis setzen
DIR="$inv"
# Gesuchter Teilstring
sea=$(basename "$1")
SEARCH_TERM=${sea:1:14}

# Alle Dateinamen ohne Endung extrahieren
mapfile -t FILENAMES < <(ls "$DIR" | sed -E 's/\.[^.]+$//')

# Variable für höchste gefundene Nummer
MAX_NUM=0
MATCH_NUM=""

for FILE in "${FILENAMES[@]}"; do
    # Suche nach übereinstimmendem Teilstring
    if [[ "$FILE" == *"$SEARCH_TERM"* ]]; then
        # Extrahiere die erste Zahl vor dem Bindestrich
        MATCH_NUM=$(echo "$FILE" | grep -oE '[0-9]+' | head -n 1)
        break
    fi
    
    # Finde höchste Zahl vor einem Bindestrich
    CUR_NUM=$(echo "$FILE" | grep -oE '^[0-9]+')
    if [[ -n "$CUR_NUM" && "$CUR_NUM" -gt "$MAX_NUM" ]]; then
        MAX_NUM=$CUR_NUM
    fi
done

# Falls ein Match gefunden wurde, frage den Nutzer
if [[ -n "$MATCH_NUM" ]]; then
    while true; do
        read -p "Soll die gefundene Zahl ($MATCH_NUM) verwendet werden? (y/n/c für Abbrechen) " choice
        case "$choice" in
            y) echo "$MATCH_NUM"; exit 0;;
            n) break;;
            c) echo "Abbruch"; exit 1;;
            *) echo "Ungültige Eingabe, bitte y, n oder c eingeben.";;
        esac
    done
fi

# Falls kein Match gefunden wurde oder der Nutzer "n" gewählt hat, erhöhe die höchste Zahl um 1 und gib sie aus
echo $((MAX_NUM + 1))
