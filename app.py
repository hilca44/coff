#!/usr/bin/env python3
import subprocess
import importlib
import work
import fu
import config as cf
import os
import datetime
import textwrap as tw
import re
import iterfzf
import json
import difflib
import json
from simple_term_menu import TerminalMenu

DEZI=0
TXT="\.txt"
ALLO="\.\d?\.tx"
TODO="\.[12345]?\.txt$"
lastFile=""

def list_files(directory=cf.DATADIR):
    return (file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)))



def inpadr():
    print("")
    print("Use only a-z 0-1 space")
    print("Client?  parts of strings, which are sure inside Address.")
    print("Example: 'lex hof fra' for Alexander Hoffmann; Hauptstr. 44; Frankfurt ")
    adr=input("> ")
    ladr=adr.strip().split(" ")
    sadr="_".join(ladr)
    return sadr


def inpprj():
    print("")
    print("Short project description. Use only a-z 0-1 space")
    adr=input("> ")
    ladr=adr.strip().split(" ")
    sadr="_".join(ladr)
    return sadr

def newOrd(x):
    filt="\.\d\.txt"
    lapa=getDirList(cf.ORDDIR, filt, "n")[0].split("/")
    lastid=lapa[0].split("_")[0]
    id=int(lastid)+1
    sadr=inpadr()
    sprj=inpprj()

    pa=str(cf.ORDDIR+str(id)+"__"+sadr+"__"+sprj+".1.txt")
    s="dd#"
    s+="\ndv# "
    s+="\nwug#0.2"
    s+="\nm0#19 12 0.3#spanplatte weiss"
    s+="\nko#"+sprj+ " lrgtb 1"
    fu.write_file(pa, s, 1)
    openvim(pa)
    return 


def newCalc(x):
    sadr=inpadr()
    spnam=inpprj()

    print("0.2 = 20% WUG")
    wug=input("WUG? [0.2]> ") or 0.2
    deli=input("Delivery Time, weeks [5]") or 5
    
    print("Material Thickness? > ")
    s=input("[19]")  or 19

    print("Material Price? > ")
    price=input() 

    print("Material Waste? > ")
    waste=input("[0.2]") or 0.2

    print("Material Name? > ")
    mname=input([ "[Melaminbesch. Spanplatte, weiß"])  or "Melaminbesch. Spanplatte wei0"

    print("Material Name? > ")
    # lli=["[k] korpus", "[i] item"]
    # terminal_menu = TerminalMenu(lli, shortcut_key_highlight_style=(["fg_yellow"]), title="typ")
    # i=terminal_menu.show()
    # tyy=["ko", "ko"]
    # ty=tyy[i]
    litem=[]
    it=""
    item=(
"ko# korpus 1 900 400 1800 0#")


    help="""
ad# {}
pr# {}
wug# {}
lief# ca. {} Wochen
m0# {} {} {}# {}# zuschn
    {}""".format(sadr, spnam, wug, deli,s,
                 price,waste,
                 mname,item)
    patth="{}{}__{}__set.txt".format(cf.DATADIR,sadr, spnam)
    fu.write_file(patth,help,openn=1)
    openvim(patth)


def getwor(arr, o):
    di={"gp": 0}
    if arr[0]=="" or arr[0]=="-":
        return
    if arr[0] in work.diwo:
        liwo=work.diwo[arr[0]]
    else:
        kee=difflib.get_close_matches(arr[0], work.diwo.keys())
        liwo=work.diwo[kee[0]]

    di["bea"]=arr
    di["epmat"]=float(liwo[0])
    di["minst"]=float(liwo[1])

    # if no amount -> calculate
    if arr[1]=="":
        di["n"]=float(liwo[2](o))
    else:
        try:
            di["n"]=float(arr[1])
        except Exception as e:
            print("wrong bea:"+" ".join(arr))
            di["n"]=1.0
    di["uni"]=liwo[3]
    di["geg"]=liwo[4]
    di["epmin"]=work.hsatz/60
    di["epzei"]=di["minst"]*work.hsatz/60
    di["mintotal"]=float(di["minst"]*di["n"])
    di["gpmat"]=di["n"]*di["epmat"]
    di["gpzei"]=di["n"]*di["epzei"]
    di["gp"]=di["gpmat"]+di["gpzei"]
    # di.row= di.n+" "+arr[3]+"  "+arr[4]+" a "+di.minst+" Euro/"+arr[3]+" = "+di.eu
    # return [di.n,di.uni,di.geg,di.ep.toFixed(2),di.gp.toFixed(2)]
    return di


def getbea2(opo):
    # print(opo["bea"])
    beas="Bearbeitungen: "
    # for e in opo["bea"]:
    # for e in opo["nOfEach"]:
    for e in opo["nOfEach"]:
        if e[0] == "" or re.findall("\d", e[0]):
            continue
        # w=getwor([e[0], e[1]], opo)["geg"]
        w=work.diwo[e][4]
        beas+= w+", "
    return beas


def getmatdescr(opo, lmas):
    k = ""
    k += "Material: {} {}mm".format(lmas[opo["mat"]]["nam"],
                                     lmas[opo["mat"]]["s"])
    return k


def makerow4faktura(opo,geg):
    geg=geg.replace("\n", "; ")
    geg=geg.replace("  ", " ")
    geg=geg.replace("  ", " ")
    geg=geg.replace("  ", " ")
    ou="\npo#{} st {} {}, {}".format(
            opo["nn"],
            opo["ep"],
            opo["nam"].upper(),
            geg,
        )
    return ou


def makerowo(opo, einzug=0):
    ou = ""
    ou += "\n"
    ou += " " * einzug
    tab = (" " * 10)
    if opo["inp"][0] == "h":
        opo["gp"]=float(opo["nn"])*float(opo["ep"])
        ou+"{} {} {} {}".format(
            opo["n"],
            opo["nam"],
            opo["ep"],
            opo["gp"],
        )
        return ou
    if opo["nn"] == -1:
        ou += fu.ff(opo["row"], 44, d=" ")
        return ou
    ll = 36
    n = fu.ff(opo["nn"], 3, 2)
    if opo["h"] != 1:
        l = fu.ff("B" + str(int(opo["w"])), 6, d=" ")
        t = "T{:<0.0f} ".format(float(opo["d"]))
        h = "H{:<0.0f} ".format(float(opo["h"]))
        # t = fu.ff("H" + str(opo["h"]), 4, d=" ")
    else:
        l = fu.ff("L" + str(int(opo["w"])), 6, d=" ")
        h = fu.ff(" ", 5, d=" ")
        t = fu.ff("T" + str(opo["h"]), 4, d=" ")
    vk = fu.ff(opo["ep"], 8, 2)
    gp = fu.ff(opo["gp"], 8, 2)
    dito = str(opo["nam"]).lower().find("dito")
    # if opo["uni"].strip() == "h":
    #     einh = fu.ff("h", 4)
    #     nam = fu.ff(opo["nam"], 33 + 15 + 9)
    #     ou += n + einh + nam + vk + gp
    if len(opo["nam"]) > ll:
        einh = fu.ff("St.", 4)
        lnam = tw.wrap(opo["nam"].upper(), ll)
        nam = fu.ff(lnam[0], 36)
        ou += n + einh + nam + l + h + t + "mm " + vk + gp
        ou += "\n" + tab
        ou += ("\n" + tab).join(lnam[1:])
    else:
        einh = fu.ff("St.", 4)
        nam = fu.ff(opo["nam"].upper(), 36)
        ou += n + einh + nam + l + h + t + " mm" + vk + gp
    opo["row"] = ou
    return ou


def getLastFi(dirr,filt,srt="e"):
    lapa=getDirList(dirr, filt,srt)[0]
    return lapa

def getDirList(patthdir, filt=".", srt="e"):
    outp = ""
    # lapa = lapa.split("/")[-1]
    lfiles = os.listdir(patthdir)
    if srt == "n":
        lfiles=sorted_alphanumeric(lfiles)
    else:
        # lfiles = sorted( lfiles,
        #     key = lambda x: os.path.getmtime(os.path.join(patthdir, x))
        #                 )
        # lfiles = list(filter(os.path.isfile, glob.glob(patthdir + "*")))
        lfiles.sort(key=lambda x: os.path.getmtime(cf.ORDDIR+x), reverse=True)
    li=list(filter(lambda x: re.search(filt.lower(), x.lower()), lfiles))
    return li
    lf2=[]
    for f in lfiles:
        if f.find(filt) !=-1:
            lf2.append(f)
    lf2=list(reversed(lf2))
    return lf2


def setfilt(x):
    v=dialogNumber("set string")
    main("o", flt=v)


def markAsPayed(fi):
    v=dialogNumber("set number")
    newfi=re.sub("\.\d?\.","."+str(v)+".", fi)
    ti="mark file with "+str(v)+"?"
    if dialog(ti):
        os.rename(fi, newfi)

    main("o", lastf=newfi)

def men(li,ke):
    while True:
        if ke<0:
            ke=0
        if ke>len(li)-1:
            ke=len(li)-1
        inh=fu.load(cf.ORDDIR+li[ke])
        print(li[ke])
        print("-"*20)
        print(inh)
        print("-"*20)
        so=["[l] next", 
            "[h] back",
            "[e] edit",
            "[k] kva", 
            "[u] nnn, STRG+r=rename, STRG+x=delete, q=quit, ", 
            "[i] Invoice", 
            "[d] Delivery Note", 
            "[p] Pdf", 
            "[1] mark as ordered",
            "[2] mark as deelivered",
            "[3] mark as payed",
            ]
        ti="ERROR"
        pa=cf.ORDDIR+li[ke]
        terminal_menu = TerminalMenu(so,
                shortcut_key_highlight_style=(["fg_yellow"]), 
                title="coff-0.4")
        i=terminal_menu.show()
        if i is None:
            return None
        doo=[
            [men,[li,ke+1]],
            [men,[li,ke-1]],
            [openvim,[pa]],
            [kva,[pa]], 
            [os.system,[ cf.FILEMAN+" "+cf.ORDDIR+ li[ke]]],
            [inv,[pa]],
            [deliv,[pa]],
            [xdgopen,[cf.ORDDIR, ".pdf"]],
            [markAsPayed,[li, ke, 1]],
            [markAsPayed,[li, ke, 2]],
            [markAsPayed,[li, ke, 3]],
            ]
        os.system("clear")
        if i <2:
            return doo[i][0](*doo[i][1])
        else:
            doo[i][0](*doo[i][1])

def dialog(ti="dialog"):
    so=["[y] yes","[n] no"]
    terminal_menu = TerminalMenu(so,
            shortcut_key_highlight_style=(["fg_yellow"]), title=ti)
    i=terminal_menu.show()
    if i == 0 :
        return True
    return False


def dialogNumber(ti="dialog"):
    nu=input("number ")
    
    return nu


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key,reverse=True)

def getfzf(dir,filt=".", srt="e"):
    # lapa=DATAFOLDER+getDirList(DATAFOLDER, filt)[0]
    lfiles = getDirList(dir, filt, srt)
    if len(lfiles)< 1:
        return
    if "pdf" in filt or cf.FZFPREVIEW==False:
        pre=False
    else:
        pre="less "+cf.ORDDIR+"{}"
    so=["[e] edittime","[n] number"]
    ti="sorting"
    terminal_menu = TerminalMenu(so,
            shortcut_key_highlight_style=(["fg_yellow"]), title=ti)
    # i=terminal_menu.show()
    if srt == "n":
        lfiles=sorted_alphanumeric(lfiles)
    lapa=iterfzf.iterfzf(lfiles,exact=True, preview=pre)
    if lapa is None:
        return None
    return [lapa]

def getfzfo(k=""):
    # lapa=DATAFOLDER+getDirList(DATAFOLDER, filt)[0]
    lfiles = fu.load(cf.DATADIR+"/2024-order.txt")
    lfiles=lfiles.split("##")
    lapa=iterfzf.iterfzf(lfiles)
    if lapa is None:
        return None
    return cf.DATADIR+lapa


def openvim(pa, config=0):
    if type(pa)==list:
        pa=pa[0]
    if config==1:
        os.system(cf.TEXTEDITOR+" -O "+ pa+" "+cf.APPDIR+"/config.py")
    else:
        subprocess.call([cf.TEXTEDITOR, pa])
    return ["", ""]

def copyo(pa, pa2):
    os.system("cp "+pa +" "+pa2)



def xdgopen(dir,fil):
    pa=getfzf(dir, fil)
    if pa==None:
        return ""
    subprocess.call(["xdg-open", cf.ORDDIR+pa[0]])


def cal(x):
    pa=getfzf(cf.DATADIR, "_set.txt")
    if pa==None:
        return ""
    pj(pa[0])
    return [pa[0]]

def inv(pa):
    # pa=getfzf(cf.ORDDIR, "_set.txt")
    if pa==None:
        return ""
    iv(pa)
    return [pa]
    


def deliv(pa):
    # pa=getfzf(cf.ORDDIR, "_set.txt")
    if pa==None:
        return ""
    iv(pa, "LIEFERSCHEIN")
    return [pa]


def kva(pa=1):
    if pa == 1:
        pa=getfzf(cf.ORDDIR, "_set.txt")
    if pa==None:
        return ""
    iv(pa, "KOSTENVORANSCHLAG")
    return [pa[0]]
    

def edio(sort="e"):
    fil=".txt"
    pa=getfzf(cf.ORDDIR, fil,sort)
    if pa==None:
        return ""
    li=getDirList(cf.ORDDIR, fil)
    i=li.index(pa[0])
    men(li,i)
    # openvim(pa[0])
    return [pa[0]]

def edic(c):

    pa=getfzf(cf.DATADIR, "_set.txt")
    if pa==None:
        return ""
    openvim(pa[0])
    pj(pa[0])
    
    return [pa[0]]


def ausw(o,pjj, geg="", t=0):
    detai = ""
    detai+="\nAuswertung 1 St.: "+o["nme"]
    detai+="\nm2bru: {}".format(o["m2bru"])
    # for e in o["lm2"]:
    #     detai+= "\nm{:.<22} {:>8} {}".format(
    #         e,
    #         e,
    #           "m2")

    for r in o["nOfEach"]:
        detai+= "\n{:.<22} {:>8.2f} {}".format(
            r,  
            o["nOfEach"][r],
            work.diwo[fu.closestkey(work.diwo, r)][3]
            )
    detai+="\n"
    mkn=o["sumaeu"]
    h = o["sumi"] / 60
    detai += "{:.<22} {:>8.2f} Euro\n".format("Material:", o["sumaeu"])
    detai += "{1:.<22} {2:>8.{0}f} h\n".format(DEZI,"Gesamtstunden:", h)
    lohn = h * work.hsatz
    detai += "{:.<22} {:8.2f} Euro\n".format("Lohnkosten:", o["suloeu"])
    selbstk = o["suloeu"] + o["sumaeu"]
    detai += "{:.<22} {:8.2f} Euro\n".format("Selbstkosten:", selbstk)
    eurwug = selbstk * pjj["wug"]
    detai += "{:.<22} {:8.2f} Faktor\n".format("WUG: x ",pjj["wug"])
    detai += "{:.<22} {:8.2f} Euro\n".format("WUG-Betrag: = ", eurwug)
    total = selbstk + eurwug
    hmax = (total - o["sumaeu"])/46
    detai += "{:.<22} {:>8.2f} Euro\n".format("Netto(calculated):", total)
    try:
        quot = total / mkn
        detai += "{:.<22} {:8.2f}\n".format("Faktor auf Material:", quot)
    except:
        quot = "Division durch 0"
        detai += "{:.<22} {}\n".format("Faktor auf Material:", quot)
    detai += "{:.<22} {:8.2f}\n".format("(netto-mat)/46=h:", hmax)
    o["detai"]=detai
    o["ep"]=total
    o["gp"]=total*o["nn"]
    return o
    if t > 0:
        angtx += detai
    angtx += "{:.<22} {:>8.2f} Euro\n".format("Netto:", o.total)
    ustsatz = 0.19
    ust = o.total * ustsatz
    angtx += "{:.<22} {:>8.2f} Euro\n".format("USt.:", o.total * ustsatz)
    produktebrutto = o.total + ust
    angtx += "{:.<22} {:>8.2f} Euro\n".format("Brutto:", produktebrutto)
    if t > 0:
        angtx += "\nPreise ab Werkstatt\n\n"
        lieumon = o.total * 0.25
        h_lum = round(lieumon)
        angtx += "\nLieferung und Montage (geschätzt)\n\n"
        angtx += "{:.<22} {:>8.2f} Euro\n".\
            format("Netto:", lieumon)
        ustsatz = 0.19
        ust = lieumon * ustsatz
        angtx += "{:.<22} {:>8.2f} Euro\n".format("USt.:", ust)

        lieumonbrutto = lieumon + ust
        angtx += "{:.<22} {:>8.2f} Euro\n".format("Brutto:", lieumonbrutto)
        angtx += "\nHinweis: Montagezeit ist geschätzt,\n" \
                 "berechnet wird der tatsächlich benötigte Aufwand\n" \
                 " mit 46 Euro/h\n"
        angtx += "{:.<22} {:>8.2f} Euro\n"\
            .format("geschätzte Gesamtsumme:", lieumonbrutto + produktebrutto)
        angtx += "\nDer Kostenvoranschlag ist 2 Wochen gültig.\n"
    return angtx




  
def  trimInput(ko):
    ko = ko.strip()
    ko = ko.replace("  ", " ")
    return ko

def  makeLbs(ko):
    ko = ko.strip().split(" ")
    return ko

def getdetailsofpart(k,kodescr,einzug=0):
    ou = "\n"+" "*einzug
    ou += "\n"
    # ou += "{} {} St., material {} ".format(k.nam.upper(), k.n,
    #                                        k.matid)
    ou += "\n"+"nGeg/Ges Typ  GesEur = Anz Einh x Ep \n"
    ou += "-"*22
    ou += "\n{:6.1f} eu ma {:4.1f} m2, {:4.1f} eu/m2"\
        .format(
            k["sumaeu"],
            k["m2bru"],
            k["eurm2"], 
            )
    # pp(k["bea"])
    for w in k["bea"]:
        working=getwor(w,k)

        ou += "\n"*2+ "{:6} ma {:5} eu = {:4.1f} {:2} x {} eu".format(
            w[0],
            working["gpmat"],
            working["n"],
            working["uni"],
            working["epmat"],
            )
            
        # ou+="\n"*7+fu.ff(w[0],6,d=":")+" ma "+ fu.ff(working["gpmat"],6,2,".")
            
        ou += "\n"+ "{:4.1f} eu ze {:4.1f} eu = {:2.1f} mi x {:4.1f} eu".format(

            working["gp"],
            working["gpzei"],
            working["mintotal"],
            working["epmin"],

            )
    ou += "\n"+" "*einzug*4
    ou += "="*22+"\n"
    ou += "g:{:5.1f}eur m:{:5.1f} z:{:5.2f}".format(
        k["sumaeu"]+ k["suloeu"],
        k["sumaeu"],
        k["suloeu"],
        )+"\n"
    # ou +="1 Teil    {:4}min, {:5.2f}eu + {:5.2f} = {:5.2f}eur/sk\n"\
    #     .format(int(k.min),  k.mk, k.lk, k.sk)
    return ou
def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b




def if_key_add_el_def(dic, key, val):
    if key in dic:
        if type(val) is str and type(dic[key]) is str:
            # dic[key]+="/"+val
            print(val)
        elif type(val) is list and dic[key] is list:
            dic[key].extend(val)
        elif type(val) is dict and type(dic[key]) is dict:
            dic[key]=addFromChildToParent(val, dic[key])
        elif type(val) is int and dic[key] is int:
            dic[key]=int(dic[key])+val
        elif type(val) is float and dic[key] is float:
            dic[key]=float(dic[key])+val

    else:
        # if type(val) is float:
        if 1:
            dic[key] = val
    return dic



def addFromChildToParent(src,tar, excl=[]):
    for c in src.keys():
        if c not in excl:
            tar=if_key_add_el_def(tar, c, src[c])
    return tar


def getBeasFromStr(s):
    li=s.strip().split(" ")
    ll=[]
    for e in li:
        ll.append([e[:6], e[6:]])
    return ll

def newMa(row):
    di = {
        "m2":0.0,
        "m2bru":0.0,
        "bea":[]
        }
    # split rows to mat and beschlaege / bearbeitung
    libea = []
    row = trimInput(row)

    li_mat = row.split("#")
    di["id"] = li_mat[0]
    di["nam"] = li_mat[2]
    try:
        di["bea"]= getBeasFromStr(li_mat[3])
    except Exception as ee:
        print("po # name # anz w d m # beas")
    # get values from  abk        
    li= makeLbs(li_mat[1])
    di["s"] = li[0]
    di["preis"] = float(li[1])
    if len(li) > 2:
        di["verschn"] = float(li[2])
    else:
        di["verschn"] = 1.3
    return di

def pp(s):
    print("var-->")
    print(s)
    print("var-->")
    input("")


def calcmat(pa, lmas):
    pa["bea"].extend(lmas[pa["mat"]]["bea"])
    pa["umf"] = pa["w"]*2+float(pa["d"])*2
    dim=[float(pa["w"]),float(pa["d"]),float(pa["h"])]
    dim.sort(reverse=True)
    pa["dim"]=dim
    pa["m2"]=dim[0]*dim[1]/1000000
    pa["w"]=dim[0]  # w=longest
    pa["d"]=dim[1]  # d=longest 2
    # ko["m2"] += float(int(ko["w"])*int(ko["d"])/1000000)

    pa["eurm2"] = lmas[0]["preis"]
    pa["h"] = lmas[0]["s"]
    pa["m2bru"] = float(pa["m2"]*lmas[pa["mat"]]["verschn"])
    pa["matpreis"] = float(lmas[pa["mat"]]["preis"])*pa["m2bru"]
    pa["ep"] = pa["matpreis"]
    pa["sumaeu"] += pa["matpreis"]
    return pa



def newPart(nme,w = 60, d = 40, h = 1.9, 
        x = 0, y = 0, z = 0,al=0,wor=[], m=0) :
    pa = {
    "nme":nme,
    "nam":nme,
    "sumaeu":0.0,
    "suloeu":0.0,
    "sumi":0.0,
    "bea": wor,
    "nOfEach":{},
    "childr":[],
    "calc":0.0,
    "m2":0.0,
    "m2bru": 0.0,
    "eurm2":0.0,
    "ep":0.0,
    "epmat":0.0,
    "gp":0.0,
    "gg":0.0,
    "w": w,
    "d": d,
    "h": h,
    "x": x,
    "y": y,
    "z": z,
    "ox": al,  
    "oy":0.0,  
    "oz":0.0, 
    "nn": 1, 
    "s": 19,
    "m":0.0,
    "co": "wh",
    "inp": "inpuu",
    "ro":0.0,
    "mat":m,
    "lws": []
    }
    return pa

def makeParts_step1(k, pjj):
    lmas=pjj["lmas"]

    p = {
    "l": ["Seite li",k["s"], k["d"], k["h"],     
          -1, 1, 0, 
          "w", [["lochre", 2]]],
    "r": ["Seite re.",k["s"], k["d"], k["h"],    
          k["w"] - k["s"], 1,1  , 
           "w", [["lochre", 2]]],
    "g": ["Boden",k["w"], k["d"], k["s"],           
          1, 1, 1, 
          "h", [["verbin", 4]]],
    "t": ["Deckel",k["w"], k["d"], k["s"],          
          1, 1, k["h"], 
          "h", [["verbin", 4]]],
    "c": ["Fachboden",k["w"], k["d"], k["s"],       
          1, 1, 28, 
          "h", [["bodent", 4]]],
    "e": ["Boden fest",k["w"], k["d"], k["s"],   
          1, 0, float(k["h"]) / 2, 
           "h",[]],
    "b": ["Rückw.",k["w"], k["s"], k["h"],        
          0, k["d"], 1, 
          "d", [["verbin", 4]]],
    "f": ["Front",k["w"], k["s"], k["h"],           
          1, -k["s"] + 1, 1,
           "d", [["topsha", 4], ["mobgr1", 1]]],
    "v": ["Mittelseite",k["s"], k["d"], k["h"], 
          k["w"] / 2 - k["s"] / 2, 1, 1, 
          "w", [["verbin", 4]]],
    "a": ["a",k["w"], k["d"], k["s"], 
          1, 1, k["h"], 
          "h", [["verbin", 4]]]
    }
    for pp in k["j"]:
        if re.search("[0-9]", pp):
            k["childr"][-1]["nn"]=float(pp)
            continue
        if k["nobea"]==1:
            p[pp][8]=[]
        paa=newPart( *p[pp], k["mat"])
        paa=calcmat(paa,lmas)
        paa=putValFromBeasToPo(paa)
        k["childr"].append( paa )
        # k["bea"].extend(paa["bea"])
        # incl=["m2bru", "ep"]
        # k=addFromChildToParent(paa, k)
    return k
    


def newHour(pjj, row):
    lmas=pjj["lmas"]
    ko = {
        "wug":pjj["wug"],
        "sumaeu":0.0,
        "suloeu":0.0,
        "sumi":0.0,
        "nobea":0,
        "bea":[],
        "nOfEach":{},
        "childr":[],
        "lm2":[],
        "calc":0.0,
        "m2":0.0,
        "m2bru": 0.0,
        "lm2": {},
        "eurm2":0.0,
        "ep":0.0,
        "epmat":0.0,
        "gp":0.0,
        "gg":0.0,
        "s":0.0,
        "par":[],
        "parts":"",
        "pats": [],
        "bea":[]
    }

    # split rows to mat and beschlaege / bearbeitung
    libea = []
    row = trimInput(row)
    ko["inp"]=row
    ko["row"]=row

    # get values from  abk        
    lbs= row.split("#")
    ko["nam"] = lbs[1]
    ko["nme"] = lbs[1]
    ko["nn"] = float(lbs[2])
    ko["ep"] = float(lbs[3])
    return ko
### 



def newKo(pjj, row):
    lmas=pjj["lmas"]
    ko = {
        "wug":pjj["wug"],
        "sumaeu":0.0,
        "suloeu":0.0,
        "sumi":0.0,
        "nobea":0,
        "bea":[],
        "nOfEach":{},
        "childr":[],
        "lm2":[],
        "calc":0.0,
        "m2":0.0,
        "m2bru": 0.0,
        "lm2": {},
        "eurm2":0.0,
        "ep":0.0,
        "epmat":0.0,
        "gp":0.0,
        "gg":0.0,
        "s":0.0,
        "par":[],
        "parts":"",
        "pats": [],
        "bea":[]
    }

    # split rows to mat and beschlaege / bearbeitung
    libea = []
    row = trimInput(row)
    ko["inp"]=row
    ko["row"]=row

    # get values from  abk        
    lbs= makeLbs(row.split("#")[1])
    # if len(lbs)<7:
    #     return 0
    ko["nam"] = lbs[0]
    ko["nme"] = lbs[0]
    ko["j"] = lbs[1]
    ko["nn"] = float(lbs[2])
    ko["w"] = float(lbs[3])
    ko["d"] = float(lbs[4])
    ko["h"] = float(lbs[5])
    ko["mat"] = int(lbs[6])
    if "-" in row.split("#")[2]:
        ko["nobea"]=1
    try:
        ko["bea"].extend(getBeasFromStr(row.split("#")[2]))
    except Exception as err:
        print(err) 
    dim=[float(ko["w"]),float(ko["d"]),float(ko["h"])]
    dim.sort(reverse=True)
    ko["dim"]=dim

    ko=putValFromBeasToPo(ko)
    # ko=calcmat(ko,lmas)
    # ko=putValsFromChildsToPo(ko)
    return ko
### 


def newPo(row,lmas,par=[],wug=10):
    di = {
        "wug":wug,
        "sumaeu":0.0,
        "suloeu":0.0,
        "sumi":0.0,
        "bea":[],
        "nOfEach":{},
        "childr":[],
        "calc": 1,
        "m2bru":0.0,
        "eurm2":0.0,
        "ep":0.0,
        "gp":0.0,
        "par":par
    }
    # split rows to mat and beschlaege / bearbeitung
    libea = []
    row = trimInput(row)
    di["inp"]=row
    di["row"]=row
    li_mat = row.strip().split("#")

    # print(li_mat)
    if len(li_mat)< 3:
        di["calc"]=0
        return di
    di["nam"] = li_mat[1]
    # get values from  abk        
    li= makeLbs(li_mat[2].strip())
    li2=[]
    for e in li:
        intt= isfloat(e)
        if intt:
            li2.append(intt)
    di["nn"] = float(li[0])
    if len(li[1])==1:
        di["w"] = float(di["par"][li[1]])
    else:
        di["w"] = float(li[1])
    if len(li[2])==1:
        di["d"] = float(di["par"][li[2]])
    else:
        di["d"] = float(li[2])
    
    di["mat"] = int(li[3])

    if di["mat"]>10:
        di["calc"]=0
        di["h"]=li[3]
        return di
    di["bea"]= getBeasFromStr(li_mat[3])
    di["bea"].extend(lmas[di["mat"]]["bea"])
    di["umf"] = di["w"]*2+float(di["d"])*2
    di["m2"] = float(int(di["w"])*int(di["d"])/1000000)
    di["eurm2"] = lmas[0]["preis"]
    di["h"] = lmas[0]["s"]
    di["m2bru"] = float(di["m2"]*1.3)
    di["matpreis"] = float(lmas[di["mat"]]["preis"])*di["m2bru"]
    di["ep"] = di["matpreis"]
    di["sumaeu"] += di["matpreis"]
    di=putValFromBeasToPo(di)
    return di
###   
def putValFromBeasToPo(di):
    for w in di["bea"]:

        working=getwor(w,di)
        if w[0]=="" or w[0]=="-" or working=={}:
            continue
        di["ep"]+=working["gp"]
        di["sumaeu"]+=working["gpmat"]
        di["suloeu"]+=working["gpzei"]
        di["sumi"] += working["mintotal"]
        di["nOfEach"]=if_key_add_el_def(di["nOfEach"],
                                         w[0], working["n"])
    di["gp"] = di["ep"]*di["nn"]
    return di


def putValsFromChildsToParent(di):
    for c in di["childr"]:
        # working=getwor(w,di)
        # di["ep"]+=working["gp"]
        di["sumaeu"]+=c["sumaeu"]*c["nn"]
        di["suloeu"]+=c["suloeu"]*c["nn"]
        di["sumi"] += c["sumi"]*c["nn"]
        di["m2bru"] += c["m2bru"]*c["nn"]
        di["ep"] += c["ep"]*c["nn"]
        di["m2"] += c["m2"]*c["nn"]
    di["gp"] = di["ep"]*di["nn"]
    di["gp"] = di["gp"]*(1+di["wug"])
    return di



def sumPos(osum, lpos):
    # sum
    # print(lpos)
    for e in lpos:
        osum["total"]+= e["gp"]
    return osum
    
def addKoParts(s):
    if s.strip()[0]=="k":
        dd=s.strip().split("#")[2].strip().split(" ")
        w=dd[1]
        d=dd[2]
        h=dd[3]
        
        dt = {
            "s": [2, h, d, 0, "se", "lochre"],
            "m": [0, h, d, 0, "ms", "lochre verbin4"],
            "b": [1, w, d, 0, "bo", "verbin4"],
            "d": [1, w, d, 0, "de", "verbin4"],
            "f": [1, w	, d, 0, "fb", "bodetr4"],
            "r": [1, w, h, 0, "rw", "verbin6"],
            "t": [1, h, w, 0, "tu", "topfsc3"],
        }
        for e in dt:
            j=dt[e]
            k="po#{}# {} {} {} 0#{}".format(
                j[4],
                j[0],
                j[1],
                j[2],
                j[5],
                )
            s+="\n"+k
    return s


def getParentsWith3x(pjj):
    parents=pjj["inh"].strip().split("<<<")[1:]
    # parents
    for e in parents:
        e=addKoParts(e)
        prows = e.strip("\n").split("\n")
        par=newPo(prows[0],pjj["lmas"])
        pjj["parents"].append(par)
        # childs
        for ee in prows[1:]:
            pjj["parents"][-1]["childr"].append(newPo(ee, pjj["lmas"], par=par))



def pj2( mawu, rowko):
    # mawu.append(rowko)

    pjj={
        "nme":"",
        "nOfEach":{},
        "parents": [],
        "childr": [],
        "ep":0,
        "gp":0,
        "oks": {},
        "tx": [],
        "lmas": [],
        "mat":0.0,
        "nn":1,
        "lm2":[],
        "sumi":0.0,
        "m2bru":0.0,
        "suloeu":0.0,
        "sumaeu":0.0,
    }
    angtx = ""
    angtx += "\n{}\n".format(datetime.date.today())
    clbo=""
    kv=""
    detail = "\n\n"
    for r in mawu:
        # skip empty
        if re.search("^[ \s#]", r):
            continue
        ty = r.split("#")[0].strip()
        if re.search("^m",r):
            di = newMa(r)
            pjj["lmas"].append(di)
        if ty == "pr":
            project = r.split("#")[1].strip()
            pj= "Projekt: {}\n".format(project)
            # pj=text_editor(project)
            angtx += " ".join(fu.wrap_einzug(pj,80))
        if ty == "tx":
            adr = r.split("#")[1].strip()
            pjj["tx"].append(adr)
        if ty == "ad":
            adr = r.split("#")[1].strip()
            angtx += "Kunde: {}\n".format(adr)
            adr = adr
        if ty == "wug":
            wug = r.split("#")[1].strip()
            pjj["wug"]=float(wug)
            detail += "WUG: {}\n".format(wug)
            wug = float(wug)
    ko=newKo(pjj,rowko)
    if ko==None:
        # if ko == 0:
        return
    else:
        ko=makeParts_step1(ko, pjj)
        for e in ko["childr"]:
            e=ausw(e,pjj)
            pjj["childr"].append(e)
            ko=addFromChildToParent(e,ko)
            pjj=addFromChildToParent(e, pjj)
            pjj["ep"]+= e["gp"]
            pjj["lmas"][e["mat"]]["m2bru"] += e["m2bru"]
            pjj["lmas"][e["mat"]]=if_key_add_el_def(pjj["lmas"][e["mat"]], e["mat"], e["m2bru"])
            ko=if_key_add_el_def(ko, "ep", e["gp"])
        ko=putValsFromChildsToParent(ko)
        pjj["parents"].append(ko)
        ko=ausw(ko, pjj)


    # output
    detail+="\nSummen Projekt:\n######"
    pjj=ausw(pjj,pjj)
    for e in pjj["lmas"]:
        detail+="\nmmm:{}".format(e["m2bru"])
    detail+=pjj["detai"]
    detail+="\nSummen Projekt:\n######"
    for op in pjj["parents"]:
        descr=""
        # descr += getmatdescr(op, pjj["lmas"])
        detail += "\n\n################"
        detail += "\n# NEW PARENT ###"
        detail += "\n################"
        # clbo+=makerow4faktura(op)
        op = ausw(op,pjj,t=2)
        roo= makerowo(op)
        detail += makerowo(op)+"\n"
        wwoo=getbea2(op)
        holi="\n           bestehend aus: "
        for opo in op["childr"]:
            holi+=str(int(opo["nn"]))+" "+opo["nam"]+", "
        lbd="Maße ca. B{} T{} H{}mm ".format(
            op["w"],
            op["d"],
            op["h"],
        )
        mai=" Material: {} ".format(pjj["lmas"][op["mat"]]["nam"])
        dee=lbd+mai+wwoo+descr+holi
        kv+=makerow4faktura(op,dee)
        descr2 = " ".join(fu.wrap_einzug(dee,70,10))
        angtx += "\n"+descr2
        # detail += getdetailsofpart(op,"nix",einzug=2)
        detail += op["detai"]
        for opo in op["childr"]:
            # descr6 = getmatdescr(opo, pjj["lmas"])
            detail += makerowo(opo)
            # wwoo6=getbea2(opo)
            # dee6=wwoo6+descr6
            # descr26 = fu.wrap_einzug(dee6,70,10)
            # detail += "\n"+descr26
            # detail += getdetailsofpart(opo,"nix")
            # opo= ausw(opo,pjj)
            # detail += "/"+ op["nam"]+" / "+opo["detai"]
    clbo+=angtx
    # text
    for e in pjj["tx"]:
        angtx+="\n{}\n".format(e)


    # detail += holi
    detail += "---  "*11+"\n"
    detail+=clbo
    detail+=kv
    pjj["rowforiv"]=kv
    # detail += m11.makematlist(osum, time=1)
    return pjj

def pj( patth):
    lkos=[]
    osum={
        "total" :0.0,
        "lkn" :0.0,
        "mkn" :0.0,
        "totalgp" :0.0,
        "totalsk" :0.0,
        "totalmat" : 1,
        "totaleurzei" :0.0,
        "minn" :0.0,
        "liallbea" : {},
        "limat" : [],
        "liparts" : [],
        "holzli" : [],
        "korp" : [],
        "project":"",
        "diwo" : {},
        "wug" : 0.2
        }  
    ###
    pjj={
        "nme":"",
        "nOfEach":{},
        "parents": [],
        "childr": [],
        "ep":0,
        "gp":0,
        "oks": {},
        "tx": [],
        "lmas": [],
        "mat":0.0,
        "nn":1,
        "lm2":[],
        "sumi":0.0,
        "m2bru":0.0,
        "suloeu":0.0,
        "sumaeu":0.0,
    }
    inh=fu.load(patth)
    pjj["inh"]=inh
    angtx = work.briefk
    angtx += "\n{}\n".format(datetime.date.today())
    rows = inh.strip("\n").split("\n")
    clbo=""
    kv="dd#2024- \ndv#2024-  "
    detail = "\n\n"
    for r in rows:
        # skip empty

        
        if re.search("^[ \s#]", r):
            continue
        ty = r.split("#")[0].strip()
        if re.search("^m",r):
            di = newMa(r)
            pjj["lmas"].append(di)
        if ty == "pr":
            project = r.split("#")[1].strip()
            pj= "Projekt: {}\n".format(project)
            # pj=text_editor(project)
            angtx += " ".join(fu.wrap_einzug(pj,80))
        if ty == "tx":
            adr = r.split("#")[1].strip()
            pjj["tx"].append(adr)
        if ty == "ad":
            adr = r.split("#")[1].strip()
            angtx += "Kunde: {}\n".format(adr)
            adr = adr
        if ty == "wug":
            wug = r.split("#")[1].strip()
            pjj["wug"]=float(wug)
            detail += "WUG: {}\n".format(wug)
            wug = float(wug)
        # para2=r.strip().split("#")[1].strip().split(" ")
        # if len(para2)!=7:
        #     continue
        if ty == "ko":
            ko=newKo(pjj,r)
            if ko==None:
            # if ko == 0:
                continue
                return
            else:
                ko=makeParts_step1(ko, pjj)
                for e in ko["childr"]:
                    e=ausw(e,pjj)
                    pjj["childr"].append(e)
                    ko=addFromChildToParent(e,ko)
                    pjj=addFromChildToParent(e, pjj)
                    pjj["ep"]+= e["gp"]
                    pjj["lmas"][e["mat"]]["m2bru"] += e["m2bru"]
                    pjj["lmas"][e["mat"]]=if_key_add_el_def(pjj["lmas"][e["mat"]], e["mat"], e["m2bru"])
                    ko=if_key_add_el_def(ko, "ep", e["gp"])
                ko=putValsFromChildsToParent(ko)
                pjj["parents"].append(ko)
                # pjj["childr"].append(ko)
                # pjj=putValsFromChildsToParent(pjj)
                
                ko=ausw(ko, pjj)


        if ty == "h":
            h=newHour(pjj,r)
            angtx+=makerowo(h)
        if ty == "po":
            ko=newPo(r,pjj["lmas"])
            pjj["parents"].append(ko)

    # output
    detail+="\nSummen Projekt:\n######"
    pjj=ausw(pjj,pjj)
    for e in pjj["lmas"]:
        detail+="\nmmm:{}".format(e["m2bru"])
    detail+=pjj["detai"]
    detail+="\nSummen Projekt:\n######"
    for op in pjj["parents"]:
        descr=""
        # descr += getmatdescr(op, pjj["lmas"])
        detail += "\n\n################"
        detail += "\n# NEW PARENT ###"
        detail += "\n################"
        # clbo+=makerow4faktura(op)
        op = ausw(op,pjj,t=2)
        angtx += makerowo(op)
        detail += makerowo(op)+"\n"
        wwoo=getbea2(op)
        holi="\n           bestehend aus:"
        for opo in op["childr"]:
            holi+=str(opo["nn"])+" "+opo["nam"]+", "
        dee=wwoo+descr+holi
        kv+=makerow4faktura(op,dee)
        descr2 = " ".join(fu.wrap_einzug(dee,70,10))
        angtx += "\n"+descr2
        # detail += getdetailsofpart(op,"nix",einzug=2)
        detail += op["detai"]
        for opo in op["childr"]:
            # descr6 = getmatdescr(opo, pjj["lmas"])
            detail += makerowo(opo)
            # wwoo6=getbea2(opo)
            # dee6=wwoo6+descr6
            # descr26 = fu.wrap_einzug(dee6,70,10)
            # detail += "\n"+descr26
            # detail += getdetailsofpart(opo,"nix")
            # opo= ausw(opo,pjj)
            # detail += "/"+ op["nam"]+" / "+opo["detai"]
    clbo+=angtx
    # text
    for e in pjj["tx"]:
        angtx+="\n{}\n".format(e)
    osum=sumPos(osum, pjj["parents"])
    angtx += "\n-----------------\n"
    angtx += "{:.<22} {:>8.2f} Euro\n".format(
        "Netto:", osum["total"])
    ustsatz = 0.19
    ust = osum["total"] * ustsatz
    angtx += "{:.<22} {:>8.2f} Euro\n".format("USt.:", ust)
    produktebrutto = osum["total"] + ust
    angtx += "{:.<22} {:>8.2f} Euro\n".format("Brutto:", produktebrutto)
    angtx += "\nPreise ab Werkstatt\n\n"


    detail += "---  "*11+"\n"
    detail += inh+"\n"
    detail += "---  "*11+"\n"
    holi = "\n"

    detail += holi
    detail += "---  "*11+"\n"
    detail+=clbo
    detail+=kv
    # detail += m11.makematlist(osum, time=1)

    ordner = os.path.dirname(patth)
    currfi = os.path.basename(patth)[:-9]

    scriptfi = os.path.basename(__file__)[4:-3]+"_"

    # pathnew = ordner + "/calc2/detail_" + fi + osum.project[:22].strip().replace(" ", "_") + "_calc.txt"
    pathnew = patth[:-9] + "_calc.txt"
    pathnewpdf = patth[:-9] + ".pdf"
    pathnew = ordner+"/"+scriptfi+currfi + "_calc.txt"
    pathnew2 = cf.ORDDIR+"KV__"+currfi + "_set.txt"
    # fu.write_file(pathnew, angtx + detail, 1)
    fu.write_file(pathnew2, kv)
    iv(pathnew2)
    fu.fcc(pathnewpdf, angtx, lkos)
    # lessf(pathnew)


def findadr( s, abb=0):
    add=fu.load(cf.DATADIR+"a.csv")
    arr=add.split("\n")
    if "_" in s:
        ls=s.split("_")
    else:
        ls=[s]

    
    # search for the first and last 3 chars
    ee=0
    for e in arr:
        i=0
        lli=e.split(";")
        if str(s)==str(lli[0].strip()):
            ee=e
            break
        for f in ls:
            if f.lower() in e.lower():
                i+=1
                if i == len(ls):
                    ee=e
                    break
                
    if ee==0:
        return s
    # li=list(filter(lambda x: s[:3].lower() in x.lower(), arr))
    # print(len(li), li[:3])
    # if len(li)<1:
    #     return "Please check: "+s+", element "+ s[:3]+" and "+s[-3:]+" not found."
    if abb==1:
        filename=ee.split(";")[1]
        filename = re.sub("[äöüÄÖÜß]", "",filename)
        filename = re.sub("[\s,]", "_",filename)
        return filename
    ae="\n      ".join(ee.split(";")[1:])
    return ae

def findInpErr(reg, st):
    if re.search(reg, st):
        return False
    else:
        r= "check input at: "+st
        pp(r)
        return True
    
def iv( patth, doc="RECHNUNG"):
    hsatz = 50  # Stundensatz
    msatz = hsatz / 60  # Minutensatz
    WUG = 1.2
    verschn = 1.3
    pdf = 0
    lmas=[]
    lkos=[]

    angtx=fu.load(cf.HOME+"/iv.tpl")
    ord=fu.load(patth)
    # print(ord)
    ym=""
    pos=""
    net=0.0
    dd=""
    ab=0
    bez=0
    ges=0
    rows=ord.strip().split("\n")
    wugandmat=[]
    for r in rows:
        if re.search("^[ \s#]", r):
            continue
        ty = r.split("#")[0].strip()
        va = r.split("#")[1].strip()
        showdeliv=0
        i=0
        if ty == "ab":
            ab = r.split("#")[1].strip()
        if ty == "dv":
            dateinv=va
            docdate=va
            if va =="":
                dateinv=datetime.date.today()
        if r[0] == "m":
            wugandmat.append(r)
        if ty == "wug":
            wugandmat.append(r)
        if ty == "dd":
            dd=va
        if ty == "ym":
            ym=va
        if ty == "tx":
            post = r.split("#")[1].strip()
            post2=fu.wrap_einzug(post,60,ein=25,arr=0)
            pos+="\n".join(post2)
            pos+="\n"*2
        if ty == "ad":
            adr = r.split("#")[1].strip()
            angtx += "Kunde: {}\n".format(adr)
            adr = adr

        if ty == "po" or ty == "ko":
            if ty == "ko":
                reg=" *[a-z_]+ +[a-z0-9]+ +[0-9]+ +[0-9]+ +[0-9]+ +[0-9]+ +[0-9]? *\#"
                if findInpErr(reg,r[3:]):
                    continue
                pjj=pj2(wugandmat, r)
                r=pjj["rowforiv"]
                
            it = r.split("#")
            nff = it[1].strip().split(" ")
            geg = " ".join(nff[3:])
            n = nff[0].strip()
            uni = nff[1].strip()
            try:
                if ty=="ko":
                    ep = float(nff[2].strip()).__round__()
                else:
                    ep = float(nff[2].strip())
            except Exception as err:
                print("po# 1 st No number here.e on Pos. 3 of")  
                print(r)  
                print("         ^^^^        ")   
                print(err)  
                men(patth)
                input()
                # return 
            if doc =="LIEFERSCHEIN":
                ep=0

            gp=float(n)*float(ep)
            net+=gp
            # items first row
            lgeg=fu.wrap_einzug(geg,40,arr=0)
            pos+=" "*10+"{:>6}  {:^6} {:<40} {:8.2f} {:9.2f}\n".format(
                n,
                uni,
                lgeg[0],
                ep,
                gp
            )

            # items rows > 1
            if len(lgeg) >1:
                for e in lgeg[1:]:
                    pos+=" "*25+"{:58} \n".format(e)   
            pos+="\n"
    # detail += m11.makematlist(osum, time=1)
    iii=patth.split("/")[-1].split("__")[0]
    aa=patth.split("/")[-1].split("__")[1]
    # addrr=fu.closestStr(la2, aa)

    # find address
    addrr=findadr(aa)
    pj=" ".join(patth.split("/")[-1].split(".")[0].
                split("__")[2].split("_")[:-1]).upper()
    ust=net*0.19
    bru=net*1.19
    if float(ab)>0:
        bez=float(ab)*-1
        ges=bru+bez
    else:
        bez=""
        ges=""
    bank=cf.BANK
    if doc !="RECHNUNG":
        bank=""
    rep=[
        ["docdate","{}".format(dateinv)],
        ["ord", pj],
        ["dde", dd],
        ["iii", "{:>6}".format(iii)],
        ["ty", "{:>77}".format(doc)],
        ["yma", ym],
        ["ro", pos[:-3]],
        # ["net", osum["total"]],
        ["adr", addrr],
        ["bank", bank],
        ["net", "{:7.2f}".format(net)],
        ["ust", "{:7.2f}".format(ust)],
        ["bru", "{:7.2f}".format(bru)],
    ]
    for e in rep:
        angtx = angtx.replace("{{"+e[0]+"}}", str(e[1]))
    if bez=="":
        rep2=[ 
            ["abs", ""],
            ["ges", ""],
            ]
    else:
        rep2=[ 
            ["abs", "bereits gezahlt {:15.2f}".format(bez)],
            ["ges", "Rechnungsbetrag {:15.2f} Euro".format(ges)],
            ]
    for e in rep2:
        angtx = angtx.replace("{{"+e[0]+"}}", str(e[1]))
    # patth=cf.ORDDIR+patth
    ordner = os.path.dirname(patth)
    currfi = os.path.basename(patth)[:-9]

    scriptfi = os.path.basename(__file__)[4:-3]+"_"
    # pathnew = ordner + "/calc2/detail_" + fi + osum.project[:22].strip().replace(" ", "_") + "_calc.txt"
    pathnew = patth[:-9] + "_inv.txt"
    pathnewpdf = patth[:-9] + ".pdf"
    # pathnew = ordner+"/"+scriptfi+currfi + "_inv.txt"
    fu.write_file(pathnew, angtx, 1)
    fu.fcc(pathnewpdf, angtx, lkos)
    lessf(pathnew)
    # xdgopenf(pathnewpdf)
    return [patth]


def showf(f):
    inh=fu.load(f)
    print(inh)


def lessf(f):
    if f != "":
        subprocess.run(["less",f])


def order():
    pa=getfzf(cf.ORDDIR, ".txt")
    return [pa, "o"]


def rename(pa):
    os.system(cf.FILEMAN+" "+ pa)
    main("o")


def invoice(pa):
    iv(pa)


def adr():
    # get data from json
    return
    a=fu.load(cf.ORDDIR+"/o/o.json")
    aa=json.loads(a)
    aaa={}
    for e in aa:
        # for ee in aa[e]:
            # aa[e][ee]= aa[e][ee].replace('"', '')
        aaa[e]={}
        # aaa[e]["iii"]=aa[e]["iii"]
        # aaa[e]["adr"]=aa[e]["adr"].replace("\n","#")
        filename = cf.ORDDIR+"/o/"+str(e)
        
        try:
            filename+="__"+aa[e]["adr"][:15]+"__"
        except Exception as cv:
            filename+="__"+str(aa[e]["ida"])+"__"
        
        filename+="_"+  str(aa[e]["ord"])+".txt"
        filename = re.sub("[äöüÄÖÜß]", "",filename)
        filename = re.sub("[\s,]", "_",filename)
        inh="dd#"+ str(aa[e]["dde"])
        inh+="\ndv#"+ str(aa[e]["div"])
        try:
            for ee in aa[e]["ite"].split("\n"):
                if re.findall("^[0-9]",ee):
                    inh+="\npo#"+ee
                else:
                    inh+="\ntx#"+ee
        except Exception as ff:
            print("wwww")
            inh+="\npo#"+str(aa[e]["ite"])+"\n"
        fu.write_file(filename, inh,1)
    return [""]


def reloa(g):
    os.system("clear")
    importlib.reload(work)
    importlib.reload(fu)
    os.system("python3 "+__file__)


# start#################################################
def main(mkey, key=0, ccc=0, lastf=0, flt=0):
    while True:
        cicle=[TODO,ALLO,ALLO, TXT]
        sorting=["n","n", "e","e"]
        displ=["TODO","ORDbyID","ORDbyEdit", "TXT-FILES"]
        dirr=cf.DATADIR
        fun=pj
        if flt!=0:
            filt=flt
        else:
            filt=cicle[ccc]
        lf=getDirList(cf.ORDDIR, filt, srt="n")
        # for e in lf:
        #     abb=e.split("__")[1]
        #     print(e)
        #     newnme=e.replace(abb, findadr(abb,1))
        #     print(newnme)
        #     os.rename(cf.ORDDIR+e, cf.ORDDIR+newnme)
        ll=len(lf)
        if lastf==0:
            lastf=getDirList(cf.ORDDIR, ALLO)
        if key<0:
            key=0
        if key>len(lf)-1:
            key=len(lf)-1
        key2=key+cf.NROWS
        if key2 > len(lf)-1:
            key2=len(lf)
        inh=fu.load(cf.ORDDIR+lastf[0])
        print(lastf[0])
        print("-"*20)
        print(inh)
        print("-"*20)

        # from prompt_toolkit import prompt

        # text = prompt('Give me some input: ')
        # print('You said: %s' % text)
        def cic(x):
            if x <len(cicle)-1:
                
                return x+1
            else:
                return 0
        
        ti="coff-0.4 Carpenters Office \n"
        ti+=  displ[ccc]+": "+str(key)+" - "+str(key2)+" from "+ str(ll)\
            + ", Filter: "+filt
        mm={
            "x": ["[h] -",  main,  [mkey, key-cf.NROWS,ccc, lastf,flt]       ],
            "y": ["[l] +",  main,  [mkey, key2,ccc, lastf, flt]       ],
            "q": ["[q] quit",        quit,  [1]       ],
            "g": ["[g] config", os.system,   ["vim "+cf.APPDIR+"/config.py"]   ],
            "a":["[a] address", openvim, [cf.DATADIR+"a.csv"]],
            "w":["[w] work", openvim, [cf.APPDIR+"/work.py"]],
            "b":["[b] exp", openvim, [cf.DATADIR+"exp.txt"]],
            # "o":["[o] order...", main, ["o"]],
            "j":["[o] set number", markAsPayed, [cf.ORDDIR+lastf[0]]],
            "o":["[f] filter", setfilt, [1]],
            "r":["[r] reload", reloa, [1]],
            "t":["[t] help", openvim, [cf.APPDIR+"/help.txt"]],
            "e":["[e] edit", openvim, [cf.ORDDIR+lastf[0]]],
            "s":["[s] list by id", edio, ["n"]],
            
            "u":["[u] nnn, STRG+r=rename, STRG+x=delete, q=quit", rename, [cf.ORDDIR+ lastf[0]]],
            "i":["[i] invoice", inv, [cf.ORDDIR+lastf[0]]],
            "k": ["[k] kva", iv, [cf.ORDDIR+lastf[0], "KOSTENVORANSCHLAG"]],
            "l":["[c] toggle ttodo, allord, txt",  main,  [mkey, key, cic(ccc)] ],
            "f":["[z] last order: "+lastf[0], openvim, [cf.ORDDIR+lastf[0]]],
            "d":["[d] deliv", iv, [cf.ORDDIR+ lastf[0], "LIEFERSCHEIN"]  ],
            "p":["[p] pdf", xdgopen, [cf.ORDDIR,".pdf"] ],
            "n":["[n] new", newOrd, [1]],
        }
        x={
            "c":"baujlpwofr1",
            "m":"ocgarq",
            "o":"fojxyablueskidpntwgr",
            }
        
        # create list entries for list
        for ii,e in enumerate(lf[key:key2]):
            mm[str(ii)]=["["+str(ii)+"] " +str(key+ii)+" "+ e, main,  [mkey, key-cf.NROWS, ccc, [lf[key+ii]]]]
            x["o"]+=(str(ii))

        # assemble menus
        m={}
        m[mkey]=[[],[],[]]
        for e in x[mkey]:
            m[mkey][0].append(mm[e][0])
            m[mkey][1].append(mm[e][1])
            m[mkey][2].append(mm[e][2])

            
        terminal_menu = TerminalMenu(m[mkey][0],
            shortcut_key_highlight_style=(["fg_yellow"]),
            title=ti)
        i=terminal_menu.show()
        # if i ==0:
        #     key+=cf.NROWS
        # elif i ==1:
        #     key-=cf.NROWS
        # else:
        os.system("clear")

        m[mkey][1][i](*m[mkey][2][i])



# try:
if __name__ == '__main__':
    while True:

        if main(cf.FIRSTMENU) == "q":
            break
