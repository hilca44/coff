#!/bin/bash


confirm (){
    while true
    do
        read -p "Continue $1? [y/n] " -n 1 -r
        if [ "$REPLY" == "y" ]; then
                    # eval "$2"
                    break
        else    if [ "$REPLY" == "n" ]; then
                    echo "Cancelled"
                    exit 0
                fi
        fi
        done
}

bookmark(){
    lasto=$(echo "$1" > ./lasto.txt)
addo "$1"
}
export -f bookmark

getordid(){
    bn=$(basename "$1")
    bn=${bn//__/ }
    read -ra adrsh <<< "$bn"
    echo "${adrsh[0]}"
}

changedat(){
  eval $1
locdat2svr
}

# less read pdf
lesss(){
    pdftotext -layout $1 - | less
}

makenewinvid(){
    ./lookupinv.sh "$1"
# iidd="find $inv -type f -regex .*$1.*$ | sort -V"
# invid=$(getordid)

#     hi=$(ls $inv | sort -n | tail -1  )
# if [ -z "$hi" ]; then
#     h2=0
# else
# h2=$( getordid "$hi" )

# fi
# # today=$(date +"%y%m%d")

# h3=$( echo "$h2 + 1" | bc)
# echo "$h3" 
}

# rename
rename (){
    clear 
    echo /////////////////////////
    echo /// strg + c = cancel ///
    echo /////////////////////////
    echo $2
    echo rename:
    read -e -i $2 ffgg
    # echo mv $1/$2 $1/$ffgg 
    # echo mv $1 $ffgg 
    # read rr

    confirm "rename"
    mv $1/$2 $1/$ffgg 

    echo "Completed"
}


hos=$(hostname)

locshpy2svr(){
    if [ $hos != 'ch-ionos' ]; then
    rsync -av --delete -b --backup-dir=backup \
    ~/cf/sh \
    -e ssh ch@217.160.53.221://home/ch/cf
    rsync -av --delete -b --backup-dir=backup \
    ~/cf/py \
    -e ssh ch@217.160.53.221://home/ch/cf
    fi
}


svrdat2loc(){
    if [ $hos != 'ch-ionos' ]; then
    rsync -av \
    -e ssh ch@217.160.53.221://home/ch/cf/datch \
    ~/cf
    fi
}
    #  --delete -b --backup-dir=backup \


locdat2svr(){
    if [ $hos != 'ch-ionos' ]; then
    rsync -av \
    $dat \
    -e ssh ch@217.160.53.221://home/ch/cf

    fi
}
    # --delete -b --backup-dir=backup \

hello(){
    echo "Hello $1"
}

#!/bin/bash

addo() {
# Datei, in der die Einträge gespeichert werden
local lastos="./lastos.txt"

    local entry="$1"

    # Falls die Datei nicht existiert, erstelle sie
    touch "$lastos"

    # Falls der Eintrag bereits existiert, verschiebe ihn ans Ende
    if grep -Fxq "$entry" "$lastos"; then
        # Entferne den existierenden Eintrag
        grep -Fxv "$entry" "$lastos" > "$lastos.tmp"
        mv "$lastos.tmp" "$lastos"
    fi

    # Anzahl der vorhandenen Zeilen zählen
    local line_count
    line_count=$(wc -l < "$lastos")

    # Falls bereits 10 Zeilen vorhanden sind, entferne die erste Zeile (älteste)
    if [ "$line_count" -ge 10 ]; then
        tail -n 9 "$lastos" > "$lastos.tmp" && mv "$lastos.tmp" "$lastos"
    fi

    # Neuen oder verschobenen Eintrag ans Ende der Datei anhängen
    echo "$entry" >> "$lastos"
    # echo "Eintrag hinzugefügt oder verschoben: $entry"
}

