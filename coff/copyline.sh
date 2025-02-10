#!/bin/bash

source ./fu.sh

clear
echo last line:
sed -n '$p' "$lasto"
echo " "
echo add:
read -e -i "$1" nme
confirm "add this line"
echo "$nme" >> $lasto
#echo "$nme"

