#!/bin/bash
#rsync -av ~/cf -e ssh ch@217.160.53.221://home/ch

source ./fu.sh

if [ -z $1 ]; then
echo nix
else
qry=($(sed -e 's/__/ /g' <<< $1))
sho=${qry[2]}

fi
adr="find $adr"
defaultHeader="===== $adr
adr:
Editrow Show Adr Ord Pdf Todo View Rnme"

bina="\
enter:reload( less {}),\
N:execute(addadr.sh )+reload(tac $adr),\
E:execute(vim $dat/a.csv)+reload(tac $adr),\
V:toggle-preview" 

se=$( $adr | less | fzf -e -i  \
--layout=reverse \
--delimiter=/ \
--tiebreak='index' \
--with-nth=-1 \
--jump-labels='123456' \
--bind change:first \
--header "$defaultHeader" \
--bind "$bin0,$bina" \
-q "$sho"
)

