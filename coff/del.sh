#!/bin/bash
source ./fu.sh
clear
echo /////////////////////////
echo /// ATTENTION         ///
echo /////////////////////////
echo
echo "$1"
# echo mv $1/$2 $1/$ffgg
# echo mv $1 $ffgg
# read rr

# if [ "$REPLY" != "Y" ]; then
#     echo "Cancelled"
#     exit 0
# fi
confirm "completely remove"
rm "$1"

# "$2"
exit 0
