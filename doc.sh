#!/bin/bash
currfi="$2"
source ./fu.sh
kdd=$(dirname "$1")
bn=$(basename "$1")
kdir=$(dirname $kdd)
bnsplit=${bn//__/ }
read -ra adrsh <<< "$bnsplit"
# IFS=" "

# while IFS= read -r ff; do
# echo "$ff"
# done <<< "${adrsh[@]}"

addd="${adrsh[2]}"
# confirm "addr: $addd"
fll="$kdd/$bn"
###############################################
# ./setdate.sh $1 $2
echo sed -i -e "s/^[-]?$2[ ]*$/$2 $(date '+%Y-%m-%d')/" "$fll"
# confirm "date 1: $1 2: $2"
sed -i -e "s/^$2[ ]*$/$2 $(date '+%Y-%m-%d')/g" "$fll"

###############################################
if [[ $(basename "$1") =~ ^([0-9]+) ]]; then
  iii="${BASH_REMATCH[1]}"
fi




# Typzuordnung
declare -A typ=(
  ["v"]="Rechnung"
  ["k"]="Kostenvoranschlag"
  ["c"]="Auftragsbestätigung"
  ["d"]="Lieferschein"
)

# Dokumenttyp basierend auf dem zweiten Argument
docty=${typ[$2]}

bank=""
if [ $2 == 'v' ]; then
invid=$(makenewinvid "$1")
iii="$invid-$iii"
bank=$(head -n5 $usd/bank.txt)
fi
# adr=$(head -n5 "$adr/$addd.txt")

# address
adr=$(sed -n '3,7p' "$adr/$addd.txt")

echo bank "$bank"
adr2=$(echo "$adr" | sed -z 's,\n,</br>,g')
echo adr "$adr2"


##################################################

# Eingabedatei mit den Daten
eingabe_datei="$1"

# Datei, in der xxitexx ersetzt wird
ziel_datei_inh=$(< $usd/tpl/iv2.html)

# Leerer String für HTML-Tabellenzeilen
ute=""
netto=0  # Variable zur Berechnung der Summe
ord=""
ddel=""
yma=""
abschlag=""
gesamtminusabschlag=""
docty=${typ[$2]}
today=$(date +"%Y-%m-%d")
docdate="$today"

# Zeile für Zeile lesen
while IFS= read -r zeile; do
# Prüfen auf "o ", "y ", oder "d " am Anfang der Zeile


  if [[ "$zeile" =~ ^o\  ]]; then
    ord="${zeile:2}"  # Alles ab dem dritten Zeichen speichern
  elif [[ "$zeile" =~ ^y\  ]]; then
    yma="${zeile:2}"  # Alles ab dem dritten Zeichen speichern
  elif [[ "$zeile" =~ ^d\  ]]; then
    ddel="${zeile:2}" # Alles ab dem dritten Zeichen speichern
  elif [[ "$zeile" =~ ^t\  ]]; then
    text="${zeile:2}" # Alles ab dem dritten Zeichen speichern
  zeilen_html="<tr><td></td><td></td><td>$text</td><td></td><td></td></tr>"

    # Zeilen-HTML an ute anhängen
    ute+="$zeilen_html"
  fi

  # Prüfen, ob die Zeile mit einer Zahl beginnt
  if [[ "$zeile" =~ ^[0-9] ]]; then
    # Zeile in Einzelteile zerlegen
    IFS=' ' read -r -a teile <<< "$zeile"


    # Erste drei Teile extrahieren
    erstes_teil="${teile[0]}"
    zweites_teil="${teile[1]}"
    drittes_teil="${teile[2]}"

    # Rest als viertes Element zusammenfügen
    rest="${teile[@]:3}"

    # Prüfen, ob erstes und drittes Teil Zahlen sind
    if [[ "$erstes_teil" =~ ^[0-9]*[.]*[0-9]*$ ]] && [[ "$drittes_teil" =~ ^[0-9]*[.]*[0-9]*$ ]]; then
      # Multiplikation von erstem und drittem Teil
      ergebnis=$(echo "scale=2; $erstes_teil * $drittes_teil" | bc)
        ergebnis=$(echo "scale=2; $ergebnis * 1.00" | bc)
        drittes_teil=$(echo "scale=2; $drittes_teil * 1.00" | bc)

      # Summe für Netto berechnen
      netto=$(echo "scale=2; $netto + $ergebnis" | bc)
    #   netto=$((netto + ergebnis))
    else
      ergebnis="N/A"  # Wenn keine gültigen Zahlen
    fi

    # HTML-Tabellenzeile erstellen
    zeilen_html="<tr><td>$erstes_teil</td><td>$zweites_teil</td><td>$rest</td><td>$drittes_teil</td><td>$ergebnis</td></tr>"

    # Zeilen-HTML an ute anhängen
    ute+="$zeilen_html"
  fi
done < "$eingabe_datei"

# Umsatzsteuer (19% von Netto) berechnen
umsatzsteuer=$(echo "scale=2; $netto * 0.19" | bc)

# Bruttorechnungsbetrag (Netto + Umsatzsteuer) berechnen
brutto=$(echo "scale=2; ($netto + $umsatzsteuer) * 1" | bc)

# Erstellen des neuen Dateinamens mit der Endung .html
neue_datei="${eingabe_datei%.txt}"
neue_datei="$neue_datei$2.html"
ziel_datei_inh=${ziel_datei_inh/xxordxx/$ord}
ziel_datei_inh=${ziel_datei_inh/xxdoctyxx/$docty}
ziel_datei_inh=${ziel_datei_inh/xxdocdatexx/$docdate}
ziel_datei_inh=${ziel_datei_inh/xxiiixx/$iii}
ziel_datei_inh=${ziel_datei_inh/xxddexx/$ddel}
ziel_datei_inh=${ziel_datei_inh/xxymaxx/$yma}
ziel_datei_inh=${ziel_datei_inh/xxitexx/$ute}
ziel_datei_inh=${ziel_datei_inh/xxnetxx/$netto}
ziel_datei_inh=${ziel_datei_inh/xxustxx/$umsatzsteuer}
ziel_datei_inh=${ziel_datei_inh/xxbrutxx/$brutto}

ziel_datei_inh=${ziel_datei_inh/xxabsxx/$abschlag}
ziel_datei_inh=${ziel_datei_inh/xxgesxx/$gesamtminusabschlag}


ziel_datei_inh=${ziel_datei_inh/xxadrxx/$adr}
ziel_datei_inh=${ziel_datei_inh/xxbankxx/$bank}
echo "$ziel_datei_inh" > "$neue_datei"
# Kopieren der Zieldatei in die neue Datei
# echo cp "$ziel_datei" "$neue_datei"
# cp "$ziel_datei" "$neue_datei"

# Ersetzen von xxitexx in der neuen Datei
# sed -i "s/xxitexx/$ute/" "$neue_datei"

echo "HTML-Tabelle wurde erstellt mit Netto ($netto), Umsatzsteuer ($umsatzsteuer) und Brutto-Rechnungsbetrag ($brutto)."


# newfile=$(./setstatus.sh $ord $1 $2)
newfile=$(./setstatus.sh  $1 $2)
# newfile="12iiii"
echo "$neue_datei"
# angtx=$(python3 iv.py $kd $newfile $2 "$bank" "$adr2")
# htmlfn=${newfile:0:-4}.html
# pdffn=${newfile:0:-4}.pdf
pdffn=${neue_datei:0:-4}pdf
pdfbn="$(basename $pdffn)"
# echo "$angtx" > $htmlfn
# wkhtmltopdf $htmlfn $pdffn
if [ $2 == 'v' ]; then
pdftar="$inv/$invid-$pdfbn"
else
pdftar="$pdf/$pdfbn"
fi
wkhtmltopdf $neue_datei "$pdftar"
# less "$pdf/$pdbn"
# pdftotext $pdffn - | less
# confirm "print pdf"
# lp "$pdffn"
# ord=$(dirname "$1")
./c.sh "'$qis'" "'$mis'"
exit 1
# ./c.sh "find $ord"
