#!/bin/bash
# ord=$1
# fil=$2
clear 
echo /////////////////////////
echo /// strg + c = cancel ///
echo /////////////////////////
echo 
# read -e -p "rename: $1/ " -i $2 ffgg
# echo mv $1/$2 $1/$ffgg 
# echo mv $1 $ffgg 
# read rr
#getmailadr(){
ifso=$IFS

# read filenme
k="$2"
#o= $("$1" | cut -d -)
#IFS="X"

# replace all __ with space
qry=($(sed -e 's/__/ /g' <<< $2))
sho=${qry[2]}
clear

# split to arr
#  echo "${o[@]}"
#     echo "surna firs"

# adr to arr
dat=$(head -n 1 vardat.txt)
readarray -t rs < $dat/a.csv
# rs=$(split -l 1 $dat/a.csv)
# echo bbbbbb ${o[2]}
# search row
for i in "${rs[@]}";
do
IFS=";"; read -r -a qry2 <<< "$i"
sho2=${qry2[1]}

echo --
echo $sho
echo $sho2
  if [ "$sho" == "$sho2" ]; then
    ss=$qry2
    
    break
  fi
done

# read row to arr
madr="${qry2[-1]}"
if [ ${qry2[3]:0} == "H" ]; then
salut="Sehr geehrter Herr ${qry2[6]},

"
elif [ ${qry2[3]:0} == "F" ]; then
salut="Sehr geehrte Frau ${qry2[6]},

"
else
salut="Sehr geehrte Damen und Herren,

"
fi

source sh/fu.sh
subj=$2
thunderbird -compose "to=$madr,subject=$subj,\
from=carsten.hilbert@gmail.com,\
body='$salut, 

im Anhang finden Sie Ihr Dokument.',\
attachment=$1/$2"




