#!/bin/bash
#rsync -av ~/cf -e ssh ch@217.160.53.221://home/ch
# source sh/fu.sh
seldb(){

PS3="Select your db: "
select dat in ch sw
do
    case $dat in
        "ch")
            dat=/home/ch/cf/datch
           break;;
        "sw")
            dat=/home/ch/cf/datsw
           break;;
        *)
           echo "Ooops"
           break;;
    esac
done
echo "$dat" > ./vardat.txt
}

confirm "select db" "seldb"



