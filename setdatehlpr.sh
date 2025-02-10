#!/bin/bash
# dont overwrite [ ]* 
echo ${1:1:1}
source ./fu.sh
da="20"
echo year  $da"??"
read -rn2 kk
da="$da$kk-"
echo month  $da"??"
read -rn2 kk
da="$da$kk-"
echo day $da"??"
read -rn2 kk
da="$da$kk"

sed -i -e "s/^-${1:1:1}.*$/-${1:1:1} $da/" $lasto

./ord.sh "$lasto"
exit 0
