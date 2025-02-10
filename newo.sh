#!/bin/bash
source ./fu.sh
# setd="$hom"/setdate.sh
# stat="$hom"/setstatus.sh
# doc="$hom"/doc.sh
# adr="$dat"/a.csv
# pdf="$dat"/pdf

# # order id + 1
hi=$(ls $ord | sort -n | tail -1  )
h2=$(echo $hi | cut -b 1-4 )
# today=$(date +"%y%m%d")

h3=$( echo "$h2 + 1" | bc)
echo "$h2" 
echo "$h3" 
echo "name"
# adrf=$(read -r < $adr)
# ifsold="$IFS"
# echo "ifs: '$IFS'"
# IFS=";"

addr=$(eval "$qas" | fzf -i -e --tac \
        --layout=reverse \
)
read -ra ss <<< "$addr"
# read -p 'edit nme:' -e -i "${ss[1]}" nme
echo $addr
adrs=$(basename "$addr" )
# sed -i "s/;${ss[1]};/;$nme;/" $adr
# IFS=" "
# declare -l sss
# read -ra sss <<< "$nme"
# read -p 'short= nme:' -e -i "${sss[1]:0:5} ${sss[0]:0:4}" nme
# # : <<'END'
# nm=${nme// /_}
# echo "short order description"
read -p 'order description: ' des
fn="$h3  a  ${adrs%.txt}  $des"
fn=${fn// /_}
echo cp $usd/tpl/ord.tpl $ord/$fn'.txt'
echo "$fn"
confirm "new order"
mkdir -p "$addr/$fn"
cp $usd/tpl/ord.tpl $ord/$fn'.txt'
exit 1
