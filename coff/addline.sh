#!/bin/bash
source ./fu.sh

clear
echo last line:
sed -n '$p' "$1"
echo " "
echo add:
read -e  nme
confirm "add this line"
echo "$nme" >> $1
exit
#echo "$nme"

