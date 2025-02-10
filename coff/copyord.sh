#!/bin/bash
source ./fu.sh

# order id + 1
hi=$(ls $ord | sort -n | tail -1  )
echo last order: $hi
h2=$(echo $hi | cut -b 1-4 )
h3=$(($((h2)) + 1))
echo "new order id: $h3" 
echo "name"

# store current field separator
ifsold="$IFS"
echo "ifs: '$IFS'"
# IFS=";"

# read -p 'edit nme:' -e -i "${ss[1]}" nme



echo original: $1
newo=$(echo "$1" | sed -r "s^/[0-9]+^/$h3^")
# newo=$(1/%[0-9]+/$h3}
echo new order: $newo
echo " "
echo edit:
read -e -i "$newo" newoo
echo cp $1 $newoo
echo last control
confirm "edit"
cp $1 $newoo
IFS="$ifsold"
exit 1

