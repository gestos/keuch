#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime


def check_cmdline_params():
    if len(sys.argv) != 4:
        print(sys.argv[0])
        print(textwrap.fill("1. Argument muss eine HOTLINEstatistik (nicht Agenten- oder Terminierungsstatistik) sein. Diese muss viertelstuendlich aufgedroeselt sein, um eine Trennung nach Kern- und Nebenzeiten zu ermoeglichen.",80))
        print(textwrap.fill("2. Argument muss eine Outbound-AGENTENstatistik sein, hieraus wird die Gesamtzahl der Outboundcalls fuer einen Mandanten gefiltert und nach verbunden/abgebrochen gezaehlt, sowie die Zeiten summiert",80))
        print
        print(textwrap.fill("Aus den beiden Dateien (welche jeweils nur einen Tag beinhalten duerfen!) wird eine Zeile aus Inbound-Kernzeit(Anrufe, verlorene Anrufe, Zeiten) und Nebenzeit(ebenda) und Outbound(Anwahlversuche, erfolgreich/nicht erfolgreich, Zeiten) gebaut.",80))
        print
        print(textwrap.fill("3. Argument ist die Ziel-Exceldatei, dorthin wird die generierte Zeile unten eingefuegt",80))
        print
        print(textwrap.fill("Beispiel mit jetzigem Setup: ./programm[0] test_stats/archiv/1458_daily_2017-03-08.xls[1] test_stats/archiv/CE_Outbound_2017-03-08.xls[2] taegliche_hotline_halbstunden.xls[3] ",280))
        exit()
    elif not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " is not a regular file")
        exit()
    elif not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + " is not a regular file")
        exit()
    elif not os.path.isfile(sys.argv[3]):
        print(sys.argv[3] + " is not a regular file")
        exit()
    else:
        sourcefile_IB = os.path.abspath(sys.argv[1])
        sourcefile_OB = os.path.abspath(sys.argv[2])
        targetfile = os.path.abspath(sys.argv[3])
        print("source inbound:\t" + sourcefile_IB)
        print("source outbound:\t" + sourcefile_OB)
        print("target:\t" + targetfile)
        return sourcefile_IB, sourcefile_OB, targetfile

def parsedate_full(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea, hou, mnt = date_crap[0:2], date_crap[3:5], date_crap[6:10], date_crap[11:13], date_crap[14:16]
    date_clea=str(day+"."+mon+"."+yea+"."+hou+"."+mnt)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y.%H.%M") # this is a python datetime.date object
    return date_objt

def parsedate_header(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea = date_crap[0:2], date_crap[3:5], date_crap[6:10]
    date_clea=str(day+"."+mon+"."+yea)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y") # this is a python datetime.date object
    return date_objt

def filerows_into_dict(daily_file,filldict):
    sheet = xlrd.open_workbook(daily_file, formatting_info=True).sheet_by_index(0)
    sheet_date = parsedate_header(sheet.cell(1,1).value).date() # this will be the dictionary key as it is the unique overall key
    rows_start = 4
    rows_end = sheet.nrows
    rowsofdict = len(filldict)  # we'll have an index of the overall rows
    startkern = datetime.time(11,30,00)
    endkern = datetime.time(19,30,00)

    if rows_end < 4:
        print ("this seems to be an empty sheet. please check")
        rowsofdict += 1
        filldict[rowsofdict] = "empty sheet"
    else:
        for i in range(rows_start,rows_end-1):
            if int(sheet.cell(i,2).value) > 0:
                rowsofdict += 1
                timestamp = parsedate_full(sheet.cell(i,0).value) # this will be the dictionary key as it is the unique overall key
                filldict[rowsofdict] = {}
                filldict[rowsofdict]["timestamp"] = timestamp
                filldict[rowsofdict]["calweek"] = timestamp.isocalendar()[1]
                filldict[rowsofdict]["weekday"] = timestamp.strftime("%a")
                filldict[rowsofdict]["year"] = timestamp.year
                filldict[rowsofdict]["month"] = timestamp.strftime("%b")
                filldict[rowsofdict]["day"] = timestamp.day
                filldict[rowsofdict]["hour"] = timestamp.hour
                filldict[rowsofdict]["minute"] = timestamp.minute
                if timestamp.weekday() in [5,6]:
                    filldict[rowsofdict]["bzeit"] = "neben"
                elif startkern <= timestamp.time() < endkern:
                    filldict[rowsofdict]["bzeit"] = "kern"
                else:
                    filldict[rowsofdict]["bzeit"] = "neben"
                filldict[rowsofdict]["angenomme"] = int(sheet.cell(i,2).value)
                filldict[rowsofdict]["verbunden"] = int(sheet.cell(i,3).value)
                filldict[rowsofdict]["TT"] = sheet.cell(i,5).value
                filldict[rowsofdict]["ACW"] = sheet.cell(i,12).value
                filldict[rowsofdict]["HT"] = sheet.cell(i,5).value + sheet.cell(i,12).value
    return filldict,sheet_date

def filerows_into_dict_OB(daily_file):
    sheet = xlrd.open_workbook(daily_file, formatting_info=True).sheet_by_index(0)
    sheet_date = parsedate_header(sheet.cell(1,1).value).date() # this will be the dictionary key as it is the unique overall key
    rows_end = sheet.nrows
    rows_start = 4
    connects = []
    non_connects = []

    if rows_end < 4:
        print ("this seems to be an empty sheet; setting values to 0...")
        connect_ob, non_connect_ob, time_connect, time_non_connect = 0,0,0,0
    else:
        for i in range(rows_start,rows_end-1):
            if str(sheet.cell(i,2).value).startswith("1458") and str(sheet.cell(i,4).value).startswith("CONNECT"):
                connects.append(sheet.cell(i,6).value)   # Spalte 6 = nur Verbindung (TT). Groessere Abweichungen bei Verbidnungs- zu Anrufzeit, die nicht nur Klingeln sind... Einflussnahme der Agenten nur auf Verbindungszeit moeglich
            elif str(sheet.cell(i,2).value).startswith("1458") and not str(sheet.cell(i,4).value).startswith("CONNECT"):
                non_connects.append(sheet.cell(i,5).value) # auch nicht verbundene Anrufe haben Zeitaufwand, aber wie der genau gerechnet wird, geht aus Agntcntrl nicht wirklich hervor
        connect_ob=len(connects)
        non_connect_ob=len(non_connects)
        time_connect=sum(connects)/86400  # Sekunde geteilt durch 86400 ergibt eine float, die dem internen Excelforat entspricht
        time_non_connect=sum(non_connects)/86400
    return connect_ob,non_connect_ob,time_connect,time_non_connect,sheet_date

def calc_day_split(bearbeitungszeit):
    angenommen  = int()
    verbundene  = int()
    handling    = float()
    talk        = float()
    acw         = float()
    for i in sorted(doe):
        if doe[i]["bzeit"] == bearbeitungszeit:
            angenommen  += doe[i]["angenomme"]
            verbundene  += doe[i]["verbunden"]
            handling    += doe[i]["HT"]
            talk        += doe[i]["TT"]
            acw         += doe[i]["ACW"]
    verlorene = angenommen-verbundene

    writelist=[handling, talk, acw, angenommen, verbundene, verlorene]
    return writelist

def write_out(row):
    xlwt.add_palette_colour("kern_farbe", 0x21)
    target_workbook_writeable.set_colour_RGB(0x21, 152, 209, 255)
    xlwt.add_palette_colour("neben_farbe", 0x22)
    target_workbook_writeable.set_colour_RGB(0x22, 176, 255, 218)
    xlwt.add_palette_colour("ob_farbe", 0x23)
    target_workbook_writeable.set_colour_RGB(0x23, 255, 255, 178)
    
    style_datum             = xlwt.easyxf('alignment: horiz right; borders: right double, right_color 0x28, left double, left_color 0x28', num_format_str = "ddd, dd.mm.yy")
    style_calls_k           = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color kern_farbe')
    style_calls_n           = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color neben_farbe')
    style_verlo             = xlwt.easyxf('alignment: horiz centre; font: color gray25')
    style_minuten_k         = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color kern_farbe', num_format_str = "[M]:SS")
    style_minuten_n         = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color neben_farbe', num_format_str = "[M]:SS")
    style_calls_ob          = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color ob_farbe')
    style_minuten_ob        = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color ob_farbe', num_format_str = "[M]:SS")

    sheet_rw.write(row, 0, datum, style_datum)   #Datum
    sheet_rw.write(row, 1, calweek, style_verlo)   #Datum

    sheet_rw.write(row, 3, list_kern[4], style_calls_k)    # Telefonierte
    sheet_rw.write(row, 4, list_kern[0], style_minuten_k) # Gesamtzeit am Tag
    sheet_rw.write(row, 5, list_kern[1], style_minuten_k) # Telefoniezeit
    sheet_rw.write(row, 6, list_kern[2], style_minuten_k) # Nacharbeitszeit
    sheet_rw.write(row, 7, list_kern[5], style_verlo) # Verlorene
    
    sheet_rw.write(row, 9, list_nebe[4], style_calls_n)    # Telefonierte
    sheet_rw.write(row, 10, list_nebe[0], style_minuten_n) # Gesamtzeit am Tag
    sheet_rw.write(row, 11, list_nebe[1], style_minuten_n) # Telefoniezeit
    sheet_rw.write(row, 12, list_nebe[2], style_minuten_n) # Nacharbeitszeit
    sheet_rw.write(row, 13, list_nebe[5], style_verlo) # Verlorene

    sheet_rw.write(row, 15, ob_connected, style_calls_ob) # Verlorene
    sheet_rw.write(row, 16, ob_conn_time, style_minuten_ob) # Verlorene
    sheet_rw.write(row, 17, ob_non_connected, style_calls_ob) # Verlorene
    sheet_rw.write(row, 18, ob_non_conn_time, style_minuten_ob) # Verlorene
    
    target_workbook_writeable.save(target)

####################end of function definitions#####################

source_IB,source_OB,target = check_cmdline_params()

doe = dict()    # dict of everything, from here all selections (by agent, by agent and date, by hours etc) are possible
doe,datum = filerows_into_dict(source_IB,doe)
list_kern=calc_day_split("kern")
list_nebe=calc_day_split("neben")

ob_connected,ob_non_connected,ob_conn_time,ob_non_conn_time,datum2 = filerows_into_dict_OB(source_OB)

if not datum == datum2:
    print ("please feed me files for the same date")
    exit()
else:
    calweek = datum.isocalendar()[1]

target_workbook = xlrd.open_workbook(target, formatting_info=True)
targetsheet = target_workbook.sheet_by_index(0)
startrow = targetsheet.nrows

target_workbook_writeable = xlcopy.copy(target_workbook)
sheet_rw = target_workbook_writeable.get_sheet(0)

write_out(startrow)
