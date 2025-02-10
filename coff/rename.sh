#!/bin/bash
source ./fu.sh

clear 
echo /////////////////////////
echo /// strg + c = cancel ///
echo /////////////////////////
echo 
echo $1
echo rename:

read -e -i $1 ffgg
confirm "rename"
mv $1 $ffgg

echo "Completed"
exit 1



