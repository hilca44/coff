#!/bin/bash
dat=$(head -n 1 ./vardat.txt)
source ./fu.sh
# IFS=$'\n'

# rename_all_files_in_dir () {
# read -p search: se
# read -p replace: rp
# ifso=$IFS
# rs=($dat/ord/*)
# itter(){

# for e in ${rs[*]};
# do
# if [[ "$e" =~ .*$se.* ]]; then
# echo
# echo $e

# ee="${e//$se/$rp}"
# echo "$ee"
# if [ $1 = "doo" ]; then
# mv "$e" "$ee"
# fi
# fi
# done
# }
# itter dont
# confirm "rename all"
# itter doo
# IFS=$ifso
# read
# }
# rename_all_files_in_dir


###########################################
# put short adr to ord
###########################################
# rs=$dat/ord/*
IFS=$'\n'
# oi=()

while read line; do
    IFS=';' read -r -a teile <<< "$line"
    zwo="${teile[1]}"
newd="$kd/$zwo"
mkdir -p "$newd"
for teil in ${teile[@]}; do

echo "$teil" >> "$usd/adr2/$zwo.txt"
done
done < $kd/a1.csv
# for e in ${rs[@]};
#     do
#         ee=$(basename "$e")
#         de=$(dirname "$e")
#         ee=${ee//__/;}
#         # nuu=$(cut -d ' ' -f 1 <<< "$ee")
#         IFS=';' read -r -a aee <<< "$ee"
#         nuu="${aee[2]}"
#         for ii in ${oi[@]};
#     do
#         declare -a nuw
#         IFS=';' read -r -a nuw <<< "$ii"
#         nu=${nuw[0]}
#         if [ "$nuu" == "$nu" ]; then
#         echo  matcppp "$nuu=$nu"
#         mv $e "$de/${aee[0]}__${aee[1]}__${nuw[1]}__${aee[3]}" 
#         fi
# done
# done
# echo fin
# read



# exit




###########################################
# put order item to each order runs perfect
###########################################
# rs=$dat/ord/*
# IFS=$'\n'
# oi=()
# while read line; do
# oi+=("$line")
# done < $dat/chtbl_1_order_item.csv
# for e in ${rs[@]};
#     do
#         ee=$(basename "$e")
#         ee=${ee//__/ }
#         declare -a nuu
#         nuu=$(cut -d ' ' -f 1 <<< "$ee")
#         for ii in ${oi[@]};
#     do
#         declare -a nuw
#         IFS=';' read -r -a nuw <<< "$ii"
#         nu=${nuw[0]}
#         if [ "$nuu" == "$nu" ]; then
#         echo  match "$nuu=$nu"
#         echo "${nuw[1]} ${nuw[2]} ${nuw[3]} ${nuw[4]}" >> "$e"
#         fi
# done
# done
# echo fin
# read




###########################################
# put order item to each order with grep **********wonderful
###########################################
# rs=$dat/ord/*
# IFS=$'\n'
# oi=()
# while read line; do
# oi+=("$line")
# done < $dat/chtbl_2_order_item.csv
# for e in "${rs[@]}";
#     do
#         ee=$(basename "$e")
#         ee=${ee//__/ }
#         declare -a nuu
#         nuu=$(cut -d ' ' -f 1 <<< "$ee")
# # second sed=remove first column, works good
# ggg=$(grep -E "^($nuu)" $dat/chtbl_2_order_item.csv )
#         # grep -E "^($nuu)" $dat/chtbl_1_order_item.csv | \
#         # sed 's/;/ /g' | sed 's/^[^ ]*[ ]//g'  >> "$e"


# if [ -z "$ggg" ]; then
#     de=$nn
#     else
#     echo $nn
#     cp $dat/tpl/ord.tpl "$e"
#     echo "$ggg" | sed 's/;/ /g' | sed 's/^[^ ]*[ ]//g'  >> "$e"

#     fi


# done
# echo fin
# read

###########################################
# put order item to each order test grep
###########################################
# rs=$dat/ord/*
# IFS=$'\n'
# oi=()
# while read line; do
# oi+=("$line")
# done < $dat/chtbl_1_order_item.csv

#         for ii in ${oi[@]};
#     do
#     nn=$(echo "$ii" | grep -Eo '^[0-9]+')
#     if [ -z $nn ]; then
#     de=$nn
#     else
#     echo $nn
#     datei=$(find $nn"__" $dat/ord)
#     cp $dat/tpl/ord.tpl $datei
#     echo "$ii" | sed 's/;/ /g' | sed 's/^[^ ]*[ ]//g'  >> "$datei"

#     fi
#         # grep -E "^($nuu)" $dat/chtbl_1_order_item.csv | \
#         #  sed 's/;/ /g' | sed 's/^[^ ]*[ ]//g'  >> "$e"
# done
# echo fin
# read



###########################################
# write file order from tbl_2_ord
###########################################
# rs=$dat/ord/*
# IFS=$'\n'
# oi=()
# while read line; do
# oi+=("$line")
# done < $dat/chtbl_2_order.csv

#         for ii in ${oi[@]};
#     do
# echo "$ii" > "$dat/ord/$ii"
# done
# echo fin
# read