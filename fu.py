import subprocess
import os
from fpdf import FPDF
import datetime
import textwrap as tw
import work
import config as cf
import readchar
import difflib
DATAFOLDER = "/home/ch/korpcalc3/calcapp/"



def anz(o):
    return 23777

def laenge(o):
    return o["w"]/1000



def umf(o):
    m =0
    m +=2*o["dim"][0]
    m +=2*o["dim"][1]
    # m=9
    return float(m/1000)


def qm(o):
    return o["dim"][0]*o["dim"][0]/1000000

def closestkey(dic, k):
    try:
        kee=difflib.get_close_matches(k, dic.keys())
        return kee[0]
    except Exception as err:
                    print(err) 


def closestStr(li, k):
    kee=difflib.get_close_matches(k, li,cutoff=0.2)
    return kee[0]



def wcc(inp):
    import sys
    os.execv(sys.executable, ["python3"] + sys.argv)
    return



def load(patth):
    # if inp == "l":
    # pnam=input("Project Name")
    ofil = open(patth, "r")
    inh = ofil.read()
    ofil.close()
    return inh
    # else:
    #     exit()

# def anz(n, l, b):
#     st = 74
#     return [st, "st"]


# def laenge(n, l, b):
#     st = l / 1000
#     return [st, "l"]

# def umf(o,l, h):
#     st = (2 * l + 2 * h) / 1000
#     return [st, "mumf"]


# def qm(n, l, h):
#     st = l * h / 1000000
#     return [st, "qm"]

def abk(st, froom=3, ll=3):
    # return("\nRemoving vowels from the given string");
    sp=[" ", "-", "_"]
    li = str(st).split(" ")
    lin=[]
    for e in li:
        st=e
        # if len(st) <= ll:
        #     return st
        n2 = st.lower()[:froom]
        vowels = ('a', 'e', 'i', 'o', 'u', '_')
        for i, x in enumerate(st[froom:].lower()):
            if i > 0:
                if x not in vowels:
                    n2 += x

        # return("New string after successfully removed all the vowels:");
        newstrabk = n2[:ll]
        lin.append(newstrabk)
    newstrabk2 = "_".join(lin)
    return newstrabk2

def korp(k,osum):
    s = 19
    tn=1
    # korpus #######################################
    # regal# 1 42 230 17 1#t 0#r 1 2
    lka = []
    # print("r", k)
    # unterschr # 2 70 60 60 1
    k = k.replace("  ", " ")
    k = k.replace("  ", " ")

    lro = k.strip().split("#")
    geg = lro[1].capitalize()  # beschreibunng
    lko = lro[2].strip().split(" ")  # korp parameter

    # print("geg", geg)
    n = int(lko[0])
    b = int(lko[1])
    t = int(lko[2])
    h = int(lko[3])
    m = int(lko[4])  # number of materil, start with 1
    nfbo = int(int(h) / 320) - 1
    # nbod = nfbo +2
    lichteb = b - 2 * s
    lichteh = h - 2 * s

    # dictionary teile [anz, matid, bez]
    dt = {
        "s": [2, h, t, 0, "se", "lore"],
        "m": [0, lichteh, t, 0, "ms", "lore verb4"],
        "b": [1, lichteb, t, 0, "bo", "verb4"],
        "d": [1, lichteb, t, 0, "de", "verb4"],
        "f": [nfbo, lichteb, t, 0, "fb", "botr4"],
        "r": [1, lichteb, lichteh, 0, "rw", "verb6"],
        "t": [1, h, b, 0, "tu", "topf3"],
    }

    for r in dt:
        dt[r][3] = 1

    # zusatz #####[name,anz]#########################################
    lzusatzbeschreibung = {}
    # teile "s3 ma"
    for te in lro[3:]:
        # list teile s 2 ma
        lteil = te.strip().split(" ")

        tnam = lteil[0]  # s f. if  # name
        tn = float(lteil[1])  # s f. if    # anzahl
        # look if parameter isset
        # if tnam in dt:
        dt[tnam][0] = tn  # n
        lzusatzbeschreibung[tnam] = {
            "n": tn,
        }
        if len(lteil) > 2:  # material fuer zusatz
            tmat = int(lteil[2])
            dt[tnam][3] = tmat
            lteil[2] = tmat
            lzusatzbeschreibung[tnam]["mat"] = tmat
            # print("set mat  name", lteil[2])
    # calc fb
    msn = 0
    if "m" in lzusatzbeschreibung:
        mss = osum.limat[dt["m"][3]]["s"]
        msn = lzusatzbeschreibung["m"]["n"]
        lichte = (lichteb - mss * msn) / (msn + 1)

        dt["f"][0] *= (msn + 1)
        dt["f"][1] = lichte
        # set n gleiter for bod
        dt["b"][5] = "glei{} verb4".format((msn + 2) * 2)
    bht = "222"  # anz sei, anz bo, anz vo
    if len(lko) > 4:
        bht = lko[4]
    holzli = "\n"
    liholi = []
    # tt = teile s b r f
    for tt in dt:
        # j = teile(b,h,t,tt,dt)
        if dt[tt][0] > 0:
            te=dt[tt]
            row = "pos #{}# {} {} {} {} {}# {}" \
                .format(te[4], int(te[0]), te[1], te[2],
                        99, te[3], te[5])
            # print("row", row)
            liholi.append(row)
            # osum.korp.append([b, t, h, tn, msn])
    return liholi




def fcc(pathh, doc, likorps, image=0):
    """
    safe file command
    :return:
    """
    dat = open(pathh, "w")
    # try:
    dat.write(doc)
    dat.close()
    # except Exception as err:
    #     print(err)

    # save FPDF() class into
    # a variable pdf
    pdf = FPDF()
    #
    # # Add a page
    pdf.set_margins(5, 10)
    pdf.add_page("P, A4")
    if image == 1:
        for i, e in enumerate(likorps):
            pdf.image("scad_{}.png".format(i), w=40)

    # # set style and size of font
    # # that you want in the pdf
    pdf.set_font("Courier", size=cf.FONTSIZE)

    # open the text file in read mode
    f = open(pathh, "r")
    # cnt = f.readlines()
    # insert the texts in pdf

    for x in f:
        pdf.cell(200, 4, txt=x, ln=1, align='L')
    f.close()
    # save the pdf with name .pdf
    pa2 = pathh[:-3] + "pdf"

    pdf.output(pa2)
    docc = "{} saved\n".format(pathh)
    return pa2

def mkdir(pa):
    dire = os.path.dirname(pa)
    if not os.path.exists(dire):
        # print("dire", dire)
        os.makedirs(dire)
        print("dir(s) created: ")
        print(dire)

def write_file(path1, content1, hint=0, openn=0):
    """

    :param path1:
    :param content1:
    :param hint:
    :return:
    """
    mkdir(path1)
    datei2 = open(path1, "w")
    datei2.write(content1)
    if hint != 0:
        print("datei erstellt: ", "file://" + path1)
    datei2.close()
    # subprocess.call(["xdg-open", path1])
    # os.system("xdg-open " + path1)


def deci2int(st):
    rr = st.split(",")[0]
    rrr = rr.split(".")[0]
    # print("rrr", rrr)
    return int(rrr)


def flo(va):
    va = float(va)
    rr = "{:6.2f}".format(va)
    return rr


def calclen6kanten(ll, hh, ss):
    meter = ((4 * ll + 4 * hh + 4 * ss) / 1000)
    return meter


def turnmin2h(mmin):
    h = int(mmin / 60)
    min = int(mmin % 60)
    return "{}:{:02d}".format(h, min)


def getmatbea(row, dmat,osum):
    di = {}
    # split rows to mat and beschlaege / bearbeitung
    libea = []
    row = row.replace("  ", " ")
    li_mat_bea = row.split("#")
    di["nam"] = li_mat_bea[1]
    mat = str(li_mat_bea[2]).strip().split(" ")
    # get values from  abk
    if len(mat) < 2:
        m = dmat[li_mat_bea[1].strip()]
        mat2 = [m[2], m[0], m[1]]
    else:
        mat2 = [li_mat_bea[1]]
        for e in mat:
            mat2.append(e)
    di["s"] = int(mat[0])
    di["preis"] = float(mat[1])
    if len(mat) > 2:
        di["verschn"] = float(mat[2])
    else:
        di["verschn"] = 1.3

    # mat bea
    if len(li_mat_bea) > 3:
        if li_mat_bea[3] != "":
            be = li_mat_bea[3].strip().split(" ")
            for w in be:
                wor = w[:4]
                worn = w[4:]
                if worn == "":
                    worn = 0
                libea.append([wor, worn, 0])  # 0=materialzaehler

    di["bea"] = libea
    return di

# class Korp:

#     def __init__(self, row, typ=""):
#         # super().__init__(diwo, hsatz, verschn, wug)
#         self.rowo = ""  # row output
#         self.nam = ""
#         self.typ = typ  # p=part k=korpus nokorp=self.n=1
#         self.n = -1
#         self.l = 1
#         self.h = 1
#         self.z = 0
#         self.bea = []
#         self.m2n = 0.0
#         self.m2 = 0.0
#         self.m2brutto=0
#         self.uml1 = 0.0
#         self.uml = 0.0
#         self.matid = 99
#         self.matnam = ""
#         self.mats = ""
#         self.matpreis = 0.00
#         self.matbea = []
#         self.matbea2 = []
#         self.keurmat = 0
#         self.eurmin = 0
#         self.eurbea = 0
#         self.min = 0
#         self.minn = 0
#         self.eurm2=0
#         self.sk = 0  # selbstk
#         self.mk = 0  # materialk
#         self.mkn = 0  # materialk
#         self.lk = 0  # lohnk
#         self.lkn = 0  # lohnk
#         self.ep = 0
#         self.total=0
#         self.gp = 0
#         self.einh = "St."
#         self.eurh = 0
#         self.row = row
#         self.meterware = 0
#         if not "#" in row:
#             return
#         self.lima = osum.limat
#         self.bea2 = []
#         self.matbea = []
#         self.matbea2 = []
#         # self.bea2.append(["mate", 1, 0])
#         # self.bea2.append(["zusc", 1, 0])
#         self.getvalues(osum)
#         if typ == "p" or typ == "po":  # no korp
#             self.calcbea(osum.diwo)
#             self.calcm2(osum)
#             self.calcmk()
#             self.calclk()
#             self.calcsk()
#             self.calcep(osum)
#             self.calcgp()
#             self.collectholzli(osum)

#     def collectholzli(self, osum):
#         r = [self.nam, self.n, self.l, self.h]
#         osum.holzli.append(r)

#     def getvalues(self, osum):
#         # split rows to mat and beschlaege / bearbeitung
#         row = self.row.replace("  ", " ")
#         lcat = row.split("#")
#         # print(str(self.n)+self.row, "nam")

#         # self.einh = str(lcat[0]).strip()
#         ldim = str(lcat[2]).strip().split(" ")
#         self.nam = lcat[1]
#         self.n = float(ldim[0])
#         # if self.typ == "nokorp":
#         #     self.n = 1
#         self.l = float(ldim[1])

#         # anz eur
#         # h, last value is eurh
#         if self.einh == "h":
#             self.ep = float(ldim[1])
#             self.eurh = float(ldim[1])
#             self.gp = self.ep * self.n
#             return
#         elif len(ldim) == 2:
#             self.ep = float(ldim[1])
#             self.eurh = float(ldim[1])
#             self.gp = self.ep * self.n
#             return
#         elif len(ldim) == 4:
#             self.matid = int(ldim[-1]) - 1
#             self.matbea = osum.limat[self.matid]["bea"].copy()  # bbea from mat
#             self.matpreis = self.lima[self.matid]["preis"]

#         # matid is last value
#         else:
#             self.matid = int(ldim[-1]) - 1
#             self.matbea = osum.limat[self.matid]["bea"].copy()  # bbea from mat
#             self.matpreis = self.lima[self.matid]["preis"]

#         # z
#         if self.einh == "ko":
#             self.z = int(ldim[3])
#         else:
#             self.z = self.lima[self.matid]["s"]

#         # meterware
#         if len(ldim) == 3:
#             self.h = 1
#             self.meterware = 1
#         else:
#             self.h = int(ldim[2])
#         for e in self.matbea:
#             # print("materialbbea", e)
#             self.bea2.append(e)

#         # mat bea

#         if len(lcat) > 3:
#             if lcat[3] != "":  # prevent empty bea
#                 be = lcat[3].strip().split(" ")
#                 # print("bbbbb",be)
#                 for w in be:
#                     wor = w[:4]
#                     worn = w[4:]
#                     if worn == "":
#                         worn = 1
#                     worn = float(worn)
#                     self.bea2.append([wor, worn, 0])  # 0=materialzaehler

#     def calcbea(self, dibea ):
#         # print(self.bea2)
#         for b in self.bea2:
#             bear = b[0]
#             n = int(b[1])  # f.i. topf4
#             rowwork = dibea[bear]
#             # unit laenge m2 umf
#             unit = rowwork[2]
#             if unit == "laenge":
#                 lst = laenge(n, self.l, self.h)
#             elif unit == "umf":
#                 lst = umf(n, self.l, self.h)
#             elif unit == "qm":
#                 lst = qm(n, self.l, self.h)
#             elif unit == "anz":
#                 lst = anz(n, self.l, self.h)

#             nbea = lst[0]
#             einh = lst[1]

#             eu = nbea * rowwork[0]
#             mi = nbea * rowwork[1]

#             eurn = eu
#             self.eurbea += eu
#             self.min += mi
#             di = {
#                 "bea": bear,
#                 "bearb": rowwork[4],
#                 "einh": einh,
#                 "anz1": round(nbea, 1),
#                 "eurmat1": round(eu, 2),
#                 "min1": round(mi),
#             }
#             # print(di)
#             self.bea.append(di)

#     def calcep(self, osum):
#         if self.einh == "h":
#             self.ep = self.eurh
#         else:
#             self.ep = int(self.sk + (self.sk * osum.wug))


#     def calclk(self):
#         self.minn = self.min * self.n
#         self.lk = round(self.min / 60 * config.hsatz, 2)
#         self.lkn = self.lk * self.n

#     def calcsk(self):
#         self.sk = round(self.mk+self.lk, 2)

#     def calcmk(self):
#         self.mk = round(self.eurbea+self.eurm2, 2)
#         self.mkn = self.mk * self.n

#     def calcgp(self):
#         self.gp = self.ep * self.n
#         self.total += self.gp

#     # def getmatbea(self):
#     #     # print("matid",self.matid)
#     #     self.matbea = self.lima[self.matid]["bea"]
#     #     self.matpreis = self.lima[self.matid]["preis"]

#     def calcm2(self, osum):
#         self.m2 = self.l * self.h / 1000000
#         self.m2n = self.m2 * self.n
#         # self.minn = self.min * self.n
#         # self.m2 = self.m21 * self.n
#         self.m2brutto = self.m2 * osum.limat[self.matid]["verschn"]
#         if self.meterware == 1:
#             self.eurm2 = self.l/1000 * self.matpreis
#         else:
#             self.eurm2 = self.m2brutto * self.matpreis
#         osum.m2[self.matid] += self.m2brutto * self.n

#         return self.m2brutto
#     def getbea2(self):
#         beas="Bearbeitungen: "
#         for e in self.bea2:
#             beas+= works.diwo[e[0]][4]+", "
#         return beas
    
#     def makerowo(self, einzug=0):
#         ou = ""
#         ou += "\n"
#         ou += " " * einzug
#         tab = (" " * 10)
#         if self.n == -1:
#             ou += ff(self.row, 44, d=" ")
#             return ou
#         ll = 36
#         n = ff(self.n, 3, 2)
#         if self.h != 1:
#             l = ff("B" + str(int(self.l)), 6, d=" ")
#             h = ff("T" + str(self.h), 5, d=" ")
#             t = ff("H" + str(self.z), 4, d=" ")
#         else:
#             l = ff("L" + str(int(self.l)), 6, d=" ")
#             h = ff(" ", 5, d=" ")
#             t = ff("T" + str(self.z), 4, d=" ")
#         vk = ff(self.ep, 8, 2)
#         gp = ff(self.gp, 8, 2)
#         dito = str(self.nam).lower().find("dito")
#         if self.einh.strip() == "h":
#             einh = ff("h", 4)
#             nam = ff(self.nam, 33 + 15 + 9)
#             ou += n + einh + nam + vk + gp
#         elif len(self.nam) > ll:
#             einh = ff("St.", 4)
#             lnam = tw.wrap(self.nam, ll)
#             nam = ff(lnam[0], 36)
#             ou += n + einh + nam + l + h + t + "mm " + vk + gp
#             ou += "\n" + tab
#             ou += ("\n" + tab).join(lnam[1:])
#         else:
#             einh = ff("St.", 4)
#             nam = ff(self.nam, 36)
#             ou += n + einh + nam + l + h + t + " mm" + vk + gp
#         self.rowo = ou
#         return ou

#     # def calcauswertung(self,total, totallk, totalmin, totalmk, hsatz, wug, t=0):
#     #     ############################
#     #     angtx = "\n" + "=" * 22
#     #     angtx += "\n{:14} {:>8.2f} Euro\n".format("Netto:", self.gp)
#     #     ustsatz = 0.19
#     #     ust = total * ustsatz
#     #     angtx += "{:14} {:>8.2f} Euro\n".format("USt.:", ust)
#     #     angtx += "{:14} {:>8.2f} Euro\n".format("Gesamtpreis:", total + ust)
#     #     if t > 0:
#     #         h = totalmin / 60
#     #         angtx += "{:14} {:>8.1f} h\n".format("Gesamtstunden:", h)
#     #         angtx += "{:14} {:>8.2f} Euro\n".format("Material:", totalmk)
#     #         lohn = h * hsatz
#     #         angtx += "{:14} {:8.2f} Euro\n".format("Lohnkosten:", totallk)
#     #         selbstk = totallk + lohn
#     #         angtx += "{:14} {:8.2f} Euro\n".format("Selbstkosten:", selbstk)
#     #         eurwug = selbstk * wug
#     #         angtx += "{:14} {:8.2f} Faktor\n".format("WUG: x ", wug)
#     #         angtx += "{:14} {:8.2f} Euro\n".format("WUG-Betrag: = ", eurwug)
#     #         quot = total / totalmk
#     #         angtx += "{:14} {:8.2f}\n".format("Faktor auf Material:", quot)
#     #
#     #     return angtx

def wrap_einzug(tex, wid, ein=0, arr=0):
    tx = tw.wrap(tex, wid,initial_indent=" "*ein,
                 subsequent_indent=" "*ein,)
    if arr ==1:
        return tx
    
    tx2 = "\n".join(tx)
    tx2=tx

    return tx2


def ff(v, w, t=0, b=0, d="."):
    """

    :param v: content
    :param w: width
    :param t: type 0=text 1=int 2=float
    :param a: align 0=left 1=right
    :return:
    """
    if b == 0:
        inn = " "
    else:
        inn = " \n"
    if t == 0:
        j = "{}".format(v).ljust(w,d) + inn

    elif t == 1:
        j = "{}".format(int(v)).rjust(w) + inn
    elif t == 2:
        j = "{:.2f}{}".format(v, inn).rjust(w)

    return j


class Sum:
    def __init__(self):

        self.total = 0
        self.lkn = 0
        self.mkn = 0
        self.totalgp = 0
        self.totalsk = 0
        self.totalmat = 1
        self.totaleurzei = 0
        self.minn = 0
        self.liallbea = {}
        self.limat = []
        self.liparts = []
        self.holzli = []
        self.korp = []
        self.m2=[]
        self.project=""
        self.diwo = {}
        self.wug = 0.2


