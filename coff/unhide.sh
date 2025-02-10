#!/bin/bash
# ord=$1
# fil=$2
source sh/fu.sh
clear 
echo mv 
echo $1/$2 
echo $1/${2:1}
confirm "unhide"
mv $1/$2 $1/${2:1}
locdat2svr





