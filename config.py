import os

HOME = os.path.dirname(__file__)+"/coff_data"
# HOME = os.path.expanduser("~/coff_data/")
ORDDIR = HOME+"ord/"
DATADIR=HOME+"calcapp/"

TEXTEDITOR="vim" 

# o or c
FIRSTMENU="o"

NROWS=5

# False or True
FZFPREVIEW=False

FONTSIZE=10.5
FILEMAN="nnn "

BANK="""
      Bitte zahlen Sie nach Erhalt der Rechnung, ohne Abzug.
      Carsten Hilbert, Skatbank
      IBAN: DE80 8306 5408 0004 8447 26
      Steuernummer: 014 827 65988
"""
DOCTEMPLATE="~/"
