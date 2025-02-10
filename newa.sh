#!/bin/bash
# dont overwrite [ ]* 

source ./fu.sh
echo "$mna"
da=""
echo name  $da"??"
read -r kk
da="$da$kk"'
'
echo street  $da"??"
read -r kk
da="$da$kk"'
'

echo postcode city $da"??"
read -r kk
da="$da$kk"


echo short5_4"??"
read -r fn

echo "$da"
confirm $da
    echo "$da" > "$adr/$fn.txt"


exit 0
