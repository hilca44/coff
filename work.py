import fu

hsatz = 50.0  # Stundensatz
msatz = hsatz / 60  # Minutensatz
wug = 0.2
verschn = 1.3
pdf = 0


briefk = """
Schreinermeister Carsten Hilbert, Mobil: 0178-5514814, carsten.hilbert@gmail.com

KOSTENVORANSCHLAG

"""

dmat = {
    "leim38eike": [38, 115, "Leimholz Eiche, keilgezinkt"],
    "daem10": [10, 12, "Dämmplatte natur"],
}

# preis beschlag pro stuek, minuten pro einh
diwo = {
    "3fachv": [200, 150, fu.anz, "St", "3fschl"],  # 3fach verriegelung incl. pz und garnitur
    "alu2x2": [5, 15, fu.laenge, "me", "Aluwinkel"],  # aluwi
    "aluw": [45, 45, fu.anz, "St", ""],  # aluwi
    "anubab": [12, 25, fu.anz, "St", "Einbohrband"],  # anuba haustuerband
    "apau": [0, 60, fu.anz, "St", "Arbeitsplattenausschnitt"],  # cnc, einpressen
    "apumle": [3, 20, fu.anz, "St", "Umleimer f. Arbeitspl."],  # cnc, einpressen
    "apverb": [6, 60, fu.anz, "St", "Verbindungsfräsung einschl. Verbinder"],  # cnc, einpressen
    "apobes": [60, 60, fu.anz, "St", "Apothekerbeschlag"],  # cnc, einpressen
    "aufh": [6, 5, fu.anz, "St", "Schrankaufhänger"],  # schrankaufhänger
    "ausk": [0, 45, fu.anz, "St", ""],  # ausklinkung
    "bohrkl": [0, 0.3, fu.anz, "St", "Bohrung"],  # cnc bohr 18
    "bo18": [0, 3, fu.anz, "St", ""],  # cnc bohr 18
    "bodent": [0.2, 1, fu.anz, "St", "Bodenträger 5mm"],  # bodentr
    "cncmin": [0, 1.5, fu.anz, "min", "CNC-Bearbeitungen"],  # cnc bearbeitung minuten
    "db12": [0.2, 4, fu.anz, "St", ""],  # duebel 12mm
    "db8h": [0.2, 1, fu.anz, "St", "Dübelverbindung"],  # duebel 8mm
    "euki": [15, 15, fu.anz, "St", ""],  # eurokiste
    "fase": [0, 1.5, fu.umf, "St", ""],  # fase berechnet kantenfu.laenge
    "falz": [0, 1.5, fu.laenge, "me", "Falz fräsen"],  # fase berechnet kantenfu.laenge
    "formfr": [0, 3, fu.umf, "me", "Formfräsen"],  # folie
    "fuscam": [6, 5, fu.anz, "St", "Stellfuß in Bohrung 200kg"],
    "gehrla": [0, 20, fu.anz,"St", "Gehrung sägen"],  # gehrung
    "gehrku": [0, 5, fu.anz, "St", "Leiste auf Gehrung sägen"],  # gehrung
    "gele": [0, 5, fu.anz, "St", "Gehrung"],  # Gehrung Leiste
    "gitt": [65, 45, fu.anz, "St", ""],  # luftgitter
    "glal": [10, 0, fu.umf, "me", "Glasleisten,"],  # frei pos mat
    "glei": [2, 5, fu.anz, "St", "Möbelgleiter"],  # gleiter moebel
    "hobl": [0, 2, fu.anz, "St", ""],  # hobeln je meter
    "htdi": [2, 15, fu.anz, "St", ""],  # haustuer dichtung, meter angeben
    "htfa": [0, 25, fu.anz, "St", ""],  # haustuer falz, meter angeben
    "htsb": [10, 25, fu.anz, "St", ""],  # haustuer schliesblech
    "kantbr": [0, 1, fu.umf, "me", "Kanten brechen"],  # 
    "klehak": [9, 15, fu.anz, "St", ""],  # kleiderhaken 3 haken
    "klesta": [12, 15, fu.anz, "St", ""],  # kleiderhaken 3 haken
    "kloz": [1, 15, fu.anz, "St", ""],  # haustuer dichtung, meter angeben
    "lack": [20, 180, fu.qm, "qm", "lackieren"],  # lackieren je m2
    "leif": [0, 12, fu.qm, "qm", ""],  # leimen flaeche pro m2
    "leimen": [0.5, 6, fu.anz, "St", "leimen"],  # leimen je meter, mittelwert aus l und h
    "lero": [7, 15, fu.anz, "St", ""],  # Lenkrolle bh 128
    "lochre": [0, 2, fu.laenge, "me", "Lochreihe"],  # lochreihe min pro m, n wird errechnet
    "mate": [1, 0, fu.qm, "qm", ""],  # frei pos mat
    "mobgr1": [8, 5, fu.anz, "St", "Möbelgriff einfach"],  # frei pos mat
    "mobgrl": [21, 10, fu.anz, "St", "Möbelgriffleiste"],  # frei pos mat
    "nutfra": [0, 1, fu.laenge, "me", "Nut fräsen"],  # nuten je m
    "oele": [10, 90, fu.qm, "qm", "oelen"],  # oelen je m2
    "rwec": [0, 3, fu.anz, "St", "Rückwand ausklinken"],  # rw ausklinkung
    "saeg": [1, 15, fu.laenge, "me", "CNC Sägeschnitt"],  # schleifen aus l und h
    "schf": [1, 15, fu.qm, "qm", "schleifen"],  # schleifen aus l und h
    "schi": [65, 45, fu.anz, "St", ""],  # laufschiene je meter
    "schl": [18, 30, fu.anz, "St", ""],  # schloss
    "schrau": [0.2, 1, fu.anz, "St", "Schraubverbindung"],  # schloss
    "skavol": [20, 15, fu.anz, "St", "Schubk..vollauszug softeinzug"],  # schiebetuerbeschlag je garnitur
    "shitu1": [20, 15, fu.anz, "St", "Schiebetürbeschlag mittel"],  # schiebetuerbeschlag je garnitur
    "shitu2": [33, 60, fu.anz, "St", "Schiebetürbeschlag mittel"],  # schiebetuerbeschlag je garnitur
    "sili": [0.5, 1.5, fu.anz, "St", ""],  #
    "socl": [0.5, 5, fu.anz, "St", ""],  # sockelclipse, 0.5 Euro je Stueck, 5 min montage
    "socaus": [0, 5, fu.anz, "St", "Sockel ausklinken"],  # sockelclipse, 0.5 Euro je Stueck, 5 min montage
    "stefus": [2, 6, fu.anz, "St", "Möbelfüße, Kunst., höhenverstellbar"],  # sockelfuss, anreissen festschr
    "tasckl": [0, 3, fu.anz, "St", "Taschenfräsung"],  # cnc tasche 40x30x40
    "topsha": [6, 8, fu.anz, "St", "Topfscharn. m. Dämpfung"],  # topfscharnier
    "umleim": [0.5, 2, fu.umf, "me", "ABS-Umleimer"],  # umleimer
    "verbin": [0.5, 2, fu.anz, "St", "Verbinder"],  # cnc, einpressen
    "zeit": [0, 1, fu.anz, "St", "Sonderarbeit (min)"],  # frei pos zeit
    "zuschn": [0, 3, fu.umf, "me", "Zuschnitt"],  # zuschnitt 4 min oder beck
}

