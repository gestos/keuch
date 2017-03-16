#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime

def check_cmdline_params():
    if len(sys.argv) != 3:
        print(sys.argv[0])
        print(textwrap.fill("1. Argument muss eine taegliche Agenten(Terminierungs-)statistik sein, oder ein Verzeichnis mit mehreren davon",80))
        print(textwrap.fill("2. Argument ist die Zieldatei, d.h. eine Exceldatei",80))
        print
        print(textwrap.fill("Beispiel mit jetzigem Setup: ./programm[0] ../test_stats/archiv/CE_alle_Agenten_taeglich_2017-03-09.xls agenten_taeglich.xls ",280))
        exit()
    elif not os.path.isfile(sys.argv[1]):
        if os.path.isdir(sys.argv[1]):
            pmode="dir"
            sourcefile_IB = os.path.abspath(sys.argv[1])
            targetfile = os.path.abspath(sys.argv[2])
            print("source inbound:\t" + sourcefile_IB)
            print("target:\t" + targetfile)
            return sourcefile_IB, targetfile, pmode
        else:
            print(sys.argv[1]+" is not a regular file")
            exit()
    elif not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + " is not a regular file")
        exit()
    else:
        pmode="file"
        sourcefile_IB = os.path.abspath(sys.argv[1])
        targetfile = os.path.abspath(sys.argv[2])
        print("source inbound:\t" + sourcefile_IB)
        print("target:\t" + targetfile)
        return sourcefile_IB, targetfile, pmode

def parsedate_header(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea = date_crap[0:2], date_crap[3:5], date_crap[6:10]
    date_clea=str(day+"."+mon+"."+yea)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y") # this is a python datetime.date object
    return date_objt

def get_filelist(folder):
    print ("scanning " + str(folder) + " ")
    agentsfiles = dict()
    for i in (s for s in os.listdir(folder) if s.endswith(".xls")):
        print ".",
        sys.stdout.flush()
        datei = os.path.join(folder,i)
        sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
        sheet_date = parsedate_header(sheet.cell(1,1).value).date() # this will be the dictionary key as it is the unique overall key
        if sheet.cell(0,0).value == "CE_alles_taeglich":
            agentsfiles[sheet_date] = datei
    print
    return agentsfiles


############## END OF FUNCTION DEFINITTIONS ############

source,target,pmode = check_cmdline_params()

if pmode == "dir":
    filelist=get_filelist(source)
    for k in sorted(filelist.keys()):
        print k,
        print filelist[k]

