#!/bin/bash
# dont overwrite [ ]* 
# $2 = d c i
sed -i -e "s/^[-]?$2[ ]*$/-$2 $(date '+%Y-%m-%d')/" $1
