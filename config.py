import os

APPDIR = os.path.dirname(__file__)
HOME = APPDIR+"/coff_data/"
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
      Max Muster, Skatbank
      IBAN: 
      Steuernummer: 
"""
DOCTEMPLATE="~/"
