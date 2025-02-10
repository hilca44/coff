#!/bin/bash
while IFS=';' read -ra li; do
while IFS=' ' read -ra i; do
    declare -l k="${i[1]}_${i[0]}"
kk="${k/' '/'_'}"
    echo ${kk:0:10}

    # process "$i"
done <<< "${li[1]}"
done < a1.csv
