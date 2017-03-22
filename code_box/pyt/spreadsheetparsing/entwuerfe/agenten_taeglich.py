#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from pandas import Series, DataFrame, ExcelWriter
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

def parsedate_full(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea, hou, mnt = date_crap[0:2], date_crap[3:5], date_crap[6:10], date_crap[11:13], date_crap[14:16]
    date_clea=str(day+"."+mon+"."+yea+"."+hou+"."+mnt)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y.%H.%M") # this is a python datetime.date object
    return date_objt

def get_cw_ma(agent_cell):
    teile = re.compile(r'(^\D)\s(.*)(\b\d[\d\s]*$)')
    agent_id_set = list()
    try:
        stdort = teile.match(agent_cell).group(1).strip()
        kuerzel = teile.match(agent_cell).group(2).strip()
        number = int(teile.match(agent_cell).group(3).strip())
        agent_id_set.extend((stdort,kuerzel,number))
    except:
        print("sth wrong with " + str(agent_cell))
    return agent_id_set

def get_filelist(folder):
    print ("scanning " + str(folder) + " "),
    agentsfiles = dict()
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    for i in (s for s in os.listdir(folder) if s.endswith(".xls")):
        sys.stdout.write(spinner.next())  # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b') 
        datei = os.path.join(folder,i)
        sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
        if sheet.nrows == 0:
            continue
        if sheet.cell(0,0) and sheet.cell(0,0).value == "CE_alles_taeglich":
            sheet_date = parsedate_header(sheet.cell(1,1).value).date() # this will be the dictionary key as it is the unique overall key
            agentsfiles[sheet_date] = datei
    print
    return agentsfiles

def read_entries(datei,doe):
    sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
    out_dict = dict()
    if sheet.nrows < 3:
        print ("that's a file without entries")
        return

    rows = sheet.nrows
    for i in range(4,sheet.nrows-1):
        stamp = parsedate_full(sheet.cell(i,0).value)
        agent = get_cw_ma(sheet.cell(i,1).value)
        year = stamp.year
        month = stamp.month
        day = stamp.day
        weekday = stamp.strftime('%a')
        hour = stamp.hour

        if weekday in ("Sat", "Sun"):
            bzeit = "n"
        else:
            if 11 < hour < 20:
                bzeit = "k"
            else:
                bzeit = "n"
        
        week = stamp.isocalendar()[1]
        angeboten = sheet.cell(i,3).value
        bearbeitet = sheet.cell(i,4).value
        verloren = angeboten - bearbeitet
        ht = sheet.cell(i,24).value
        tt = sheet.cell(i,29).value
        aht = sheet.cell(i,24).value / bearbeitet
        att = sheet.cell(i,29).value / bearbeitet
        acw = aht - att
        primkey = tuple((stamp,agent[1]))
        doe[primkey] = dict()
        o = doe[primkey]
        o["ag"] = agent[1]
        o["lo"] = agent[0]
        o["yy"] = year
        o["mm"] = month
        o["dd"] = day
        o["hh"] = hour
        o["bz"] = bzeit
        o["ww"] = week
        o["wd"] = weekday
        o["an"] = angeboten
        o["be"] = bearbeitet
        o["vl"] = verloren
        o["tt"] = tt
        o["ht"] = ht
        o["att"] = att
        o["aht"] = aht
        o["acw"] = acw
    return doe


        



############## END OF FUNCTION DEFINITTIONS ############

source,target,pmode = check_cmdline_params()
dict_o_e = dict()
if pmode == "dir":
    filelist=get_filelist(source)
    for k in sorted(filelist.keys()):
        dict_o_e = read_entries(filelist[k],dict_o_e)

#callsumme = list()
#zeitsumme = list()

#for prim in dict_o_e.keys():
#    if dict_o_e[prim]["ww"] == 9 and dict_o_e[prim]["ag"] == "tetzlva":
#        callsumme.append(dict_o_e[prim]["be"])
#        zeitsumme.append(dict_o_e[prim]["tt"])

writer = ExcelWriter(target)
frame = DataFrame(dict_o_e)
frame1 = DataFrame.transpose(frame)
kws = frame1.ww.unique()
monate = frame1.mm.unique()
cols = list(frame1.columns.values)
print cols
frame1=frame1[['ww','wd', 'lo', 'ag', 'be','att', 'acw', 'aht', 'bz', 'vl']]

for woche in kws:
    srow = xlrd.open_workbook(target, formatting_info=True).sheet_by_index(0).nrows+1
    kw = (frame1[frame1.ww == woche])
    kw.to_excel(writer,'Colors',startrow=srow,header=False,index=False)
    writer.save()
    uniq_agents = kw.ag.unique()
    #for agent in uniq_agents:
    #    suma = kw[['be','tt']][kw.ag == agent].sum()
