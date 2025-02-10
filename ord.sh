#!/bin/bash
#rsync -av ~/cf -e ssh ch@217.160.53.221://she/ch
# sh=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )# cd $sh
ord=$(dirname "$1")
source ./fu.sh
addo "$1"

if [ -z "$1" ]; then
echo "no paramaaaaaaaaaaaaaaaaaaaaaaaaaa"
else
lasto=$(echo "$1" > ./lasto.txt)
fi
oid=$(getordid "$1")
source ./fu.sh
men="[esc]back [enter]edirow 
e edifile 
+ reload
k estimation of cost
c confirmation
d delivery note
i invoice 
n new item
r rename
y copy row
x delete
"
#View Rnme aL Jmp Nw Fmn chnGadr
#Inv Dln Kva Confrm statU [X]cford"
hh="+change-header($men\\ORD)"


u="less $1"

bin2="\
h:execute( ./c.sh 'find $ord')+abort,\
<:execute($sh/adr.sh $1),\
e:execute(vim $lasto )+reload(less $lasto)+clear-query,\
K:execute( ./setdatehlpr.sh {})+reload($u)+clear-query,\
k:execute( ./doc.sh $1 'k')+abort,\
i:execute( ./doc.sh $1 v),\
c:execute( $doc $1 c)+reload(less $ord/${1/__?__/__c__})+clear-query,\
d:execute( $doc $1 d)+reload(less $ord/${1/__?__/__d__})+clear-query,\
n:execute(./addline.sh $lasto)+reload($u),\
y:execute(./copyline.sh {})+reload($u),\
o:execute(./copyord.sh $lasto)+reload($u),\
s:execute($sh/sealine.sh $lasto)+abort+execute($sh/ord.sh $1),\
j:jump-accept,\
enter:execute(./edistr.sh $lasto {} )+reload($u)+clear-query,\
r:execute(./rename.sh $lasto )+abort,\
x:execute($sh/del.sh $ord $1 )+abort\
"
bin="$bin0,$bin2"

# read -rsn1 kk
# echo $kk was pressed


se=$( "$u" | fzf -e -i \
--jump-labels='0123456789abfghilmno' \
--layout=reverse \
--print-query \
--header "$men0 $kff $moo $1" \
--bind "$bin" )



