#!/bin/bash
hom=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $hom
ifso=$IFS
IFS=$'\n'

# put all files in dir to array
# rs=(~/cf/ord/*) 
# arr=(k c v p)
# for e in ${rs[*]};
# do

# for f in ${arr[*]};
# do
#     echo $e
# ee="${e/_/__}"
#     echo "${ee}"

#     # sed -i -e "s/^d$f/-$f /" $e
#     sed -i -e "s/^d$f/-$f /" $e
#     #mv "$e" "$ee"
# done
# done
umlaut () {
    nme="$1"
    nme=${nme//[ -\.]/_}
    nme=${nme//ü/ue}
    nme=${nme//ö/oe}
    nme=${nme//ä/ae}
    nme=${nme//ß/ss}
echo $nme
}

# func person
makeshortperson () {
    declare -l words
IFS=" "
read -ra words <<< "$1"
IFS=$ifso
# slice nam
last=${words[-1]}
if [ ${#words[@]} -gt 1 ]; then
last2=${words[-2]}
nme="${last:0:5} ${last2:0:4}"
else
nme="${words:0:10}"
fi
nme=$(umlaut "$nme")
echo $nme
}



# func company
makeshortcom () {
    declare -l words
IFS=" "
read -ra words <<< "$1"
IFS=$ifso
# slice nam
last=${words[-1]}
if [ ${#words[@]} -gt 1 ]; then
last2=${words[-2]}
nme="${words:0:5} ${last:0:4}"
else
nme="${words:0:10}"
fi
nme=$(umlaut "$nme")
echo $nme
}

aa=$(< $hom/a.csv)
for e in ${aa[@]};
do

#make short


# e=${e/;/;;;}
IFS=';'
read -a ff <<< "$e"
# ff="$f;;"
IFS=$ifso

# company
if [ ${#ff[*]} -gt 5 ]; then
# echo ${#ff[@]}
sho=$(makeshortcom "${ff[1]}")
ee="${ff[0]};$sho;${ff[1]}"

else
# person
sho=$(makeshortperson "${ff[1]}")
ee="${ff[0]};$sho;--;${ff[1]}"
fi
eea=""
for t in "${ff[@]}";do
eea="$eea
$t"
done
############################################ write file
if [ ${#ff[2]} -gt 2 ]; then
nnm=$(umlaut "${ff[2]}___${ff[3]}")
echo "$eea" > $hom/adr/$nnm.txt


fi
# sed -i -e "s/$e/$ff/"  "$fi"
# echo $e
done
read
IFS=$ifso

######################################################


# while read -ra f; do
#     # declare -l k="${i[1]}_${i[0]}"
# # kk="${k/' '/'_'}"
#     echo "${f[*]}"

#     # process "$i"
# done < "$hom/a.csv"
#     read



# aa=(cut -d$IFS $hom/a.csv)
# # read -ra aa <<< "$fi"
# echo $aa
# # read -p soso -i "$fi"
# for f in ${aa[*]};
# do
# echo "$f"
# # ff="${f/;/;;;}"
# ff="$f;;"
# echo "$ff"
#     sed -i -e "s/$f/$ff/"  "$fi"
# # lifi=$(cut -d; "$f")
# done