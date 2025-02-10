#!/bin/bash
echo "$3" > ./lastcmd.txt
if [[ "$1" == "u" ]]; then
echo "$2" > ./vardat.txt
fi
us=$(head -n 1 ./vardat.txt)
lasto=$(head -n 1 ./lasto.txt)
lastcmd=$(head -n 1 ./lastcmd.txt)
usd="./da/$us"
kd="$usd/kd"
ord="$usd/ord"
inv="$usd/inv"
pdf="$usd/pdf"
adr="$usd/adr2"
qt="find $ord -regex .+__[aekvd]__.+txt$ | sort -Vr"
qo="find $ord -type f -regex .*txt$ | sort -Vr"
qis="find $inv -type f -regex .*/[0-9].*__.*$ | sort -Vr"
qpdf="find $pdf -type f -regex .+pdf$ | sort -n"
qas="find $adr -regex .*txt$ | sort"
qlast="less ./lastos.txt | sort -Vr"
qo="grep -L 'hidden' $ord/*__*.txt | sort -Vr"
# qg="cat . | sort -Vr"
# qt="grep -LE '^[-]?[vp].+[^0-9]' $ord/*__*.txt | sort -Vr"
# qt="for file in $ord/*; do echo $(head -n 1 $file); done "

kd2=$(pwd)
m0="==$kd2=== $(hostname) $0 ===== $qy"'
'
source ./men.sh

if [[ -z "$1" ]]; then
    qy="$qt"
    menu="$mt"

else
    qy="$1"
    menu="$2"
fi
men="$m0$kff $menu"
ht="$m0 $mt"
ha="$m0 $maa"
ho="$m0 $mo"
hs="$m0 $ms"
b0="\
O:execute(xdg-open {} ),\
v:execute(./c.sh '$qis' '$mis')+abort,\
e:execute(nano {}),\
s:unbind(s,i,e,r,t,o,l,p,a,x,d,n)+change-header($hs),\
<:rebind(s,i,e,r,t,o,l,p,a,x,d,n)+change-header($ht),\
r:execute(./rename.sh {})+reload($ql),\
i:execute( ./doc.sh {} v)+change-query({}),\
d:execute( ./doc {} d)+reload($qy),\
c:execute( ./doc {} c)+reload($qy),\
t:execute(./c.sh '$qt' '$mt' t)+abort,\
o:execute(./c.sh '$qo' '$moo' o)+abort,\
l:execute(./c.sh '$qlast' '$ml' l)+abort,\
p:execute(./c.sh '$qpdf' '$mp' 'p')+abort,\
a:execute(./c.sh '$qas' '$ha' a)+abort,\
h:execute(./hide.sh {})+abort,\
x:execute(./del.sh {})"


if [[ "$lastcmd" =~ [olt] ]]; then
    
bnn=",n:execute(./newo.sh )"
elif [ "$lastcmd" == "a" ]; then
bnn=",n:execute(./newa.sh )"
else
bnn=""
fi

bin0="$b0$bnn"

source ./fu2.sh