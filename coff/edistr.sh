#!/bin/bash
source ./fu.sh

clear
echo original:
echo "$2"
echo " "
echo edit:
read -e -i "$2" nme
confirm "edit"
sed -i "s^$2^$nme^" "$1"
#echo "$nme"

# locdat2svr

