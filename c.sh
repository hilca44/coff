#!/bin/bash

source ./fu.sh


    se=$( eval "$qy" | fzf -e -i \
        --layout=reverse \
        --no-sort \
        --jump-labels='123456789' \
        --delimiter='/' \
        --query="" \
        --with-nth=-1 \
        --color fg:'#FFFF00' \
        --preview="less {}" \
        --preview-window='30%,down,border-sharp' \
        --header "$men" \
        --bind "$bin0" )

exit 0
