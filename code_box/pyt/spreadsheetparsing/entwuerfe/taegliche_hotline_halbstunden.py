#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime


def check_cmdline_params():
    if len(sys.argv) != 3:
        print(sys.argv[0])
        print(textwrap.fill("1. Argument muss ein Verzeichnis oder eine HOTLINEstatistik (nicht Agenten- oder Terminierungsstatistik) sein. Diese muss viertelstuendlich aufgedroeselt sein, um eine Trennung nach Kern- und Nebenzeiten zu ermoeglichen.",80))
        print
        print(textwrap.fill("2. Argument ist die Ziel-Exceldatei, dorthin wird die generierte Zeile unten eingefuegt",80))
        print
        print(textwrap.fill("Beispiel mit jetzigem Setup: ./programm[0] test_stats/archiv/1458_daily_2017-03-08.xls[1] taegliche_hotline_halbstunden.xls[2] ",280))
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

def excel_date(date1):
    temp = datetime.date(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

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
        if sheet.cell(0,0) and (sheet.cell(0,0).value == "Hotlineber1458Gesing taegl"):
            #if sheet.cell(0,0) and sheet.cell(0,0).value == "CE_alles_taeglich":
            sheet_date = parsedate_header(sheet.cell(1,1).value).date() # this will be the dictionary key as it is the unique overall key
            agentsfiles[sheet_date] = datei
    print
    return agentsfiles

def read_entries(datei,doe):
    sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
    out_dict = dict()
    kern_start = datetime.time(11,30)
    kern_end = datetime.time(19,15)
    if sheet.nrows < 3:
        print ("that's a file without entries")
        return

    rows = sheet.nrows
    for i in range(4,sheet.nrows-1):
        stamp = parsedate_full(sheet.cell(i,0).value)
        year = stamp.year
        month = stamp.month
        day = stamp.day
        week = stamp.isocalendar()[1]
        weekday = stamp.strftime('%a')
        hour = stamp.hour

        if weekday in ("Sat", "Sun"):
            bzeit = "n"
        elif kern_start <= stamp.time() <= kern_end:
            bzeit = "k"
        else:
            bzeit = "n"

        angeboten = sheet.cell(i,2).value
        verbunden = sheet.cell(i,3).value
        verloren = angeboten - verbunden
        tt = sheet.cell(i,5).value
        acw = sheet.cell(i,12).value
        ht = tt + acw
        
        xldate=excel_date(stamp.date())

        if angeboten > 0:
            doe[stamp] = dict()
            o = doe[stamp]
            o["dt"] = stamp.date()
            o["yy"] = year
            o["mm"] = month
            o["dd"] = day
            o["xl"] = xldate
            o["hh"] = hour
            o["bz"] = bzeit
            o["ww"] = week
            o["wd"] = weekday
            o["an"] = angeboten
            o["vb"] = verbunden
            o["vl"] = verloren
            o["tt"] = tt
            o["ht"] = ht
            o["acw"] = acw
    return doe

def target_days_found(sheet):
    found_days = [0]
    s = target_workbook.sheet_by_index(0)
    for row in range (2,s_row-1):
        c = s.cell(row,0)
        if c.value:
            found_days.append(c.value)
    return found_days

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
source,target,pmode = check_cmdline_params()
doe = dict()    # dict of everything, from here all selections (by agent, by agent and date, by hours etc) are possible

## read everything from directory into a dict and create a dataframe from it
if pmode == "dir":
    filelist=get_filelist(source)
    for k in sorted(filelist.keys()):
        doe = read_entries(filelist[k],doe)

column_order = ['dt','yy','mm','ww','wd','dd','xl','hh','an','vb','vl','ht','tt','acw','bz']
doe_frame = pandas.DataFrame(doe).T[column_order]
dates_in_dir = doe_frame.dt.unique()    # numpy.ndarray of datetime.date objects
xldates_in_dir = doe_frame.xl.unique()    # numpy.ndarray of datetime.date objects
years_in_dir = doe_frame.yy.unique()    # numpy.ndarray of year values
kws_in_dir = doe_frame.ww.unique()      # numpy.ndarray of week numbers
monate_in_dir = doe_frame.mm.unique()   # numpy.ndarray of month numbers

target_workbook = xlrd.open_workbook(target, formatting_info=True)  # this is the file
target_sheet = target_workbook.sheet_by_index(0)
target_workbook_w = xlcopy.copy(target_workbook)                # a copy is needed to write into
s_row = target_sheet.nrows+1

last_day_target = max(target_days_found(target_sheet)) # returns the highest date found as an excel date number
days_to_add = [i for i in xldates_in_dir if i > last_day_target] # list of days in scanned directory that are newer than the last day of the target sheet

print xldates_in_dir
print last_day_target
print days_to_add






# # doe,datum = filerows_into_dict(source_IB,doe)
# list_kern=calc_day_split("kern")
# list_nebe=calc_day_split("neben")
# 
# ob_connected,ob_non_connected,ob_conn_time,ob_non_conn_time,datum2 = filerows_into_dict_OB(source_OB)
# 
# if not datum == datum2:
#     print ("please feed me files for the same date")
#     exit()
# else:
#     calweek = datum.isocalendar()[1]
# 
# target_workbook = xlrd.open_workbook(target, formatting_info=True)
# targetsheet = target_workbook.sheet_by_index(0)
# startrow = targetsheet.nrows
# 
# target_workbook_writeable = xlcopy.copy(target_workbook)
# sheet_rw = target_workbook_writeable.get_sheet(0)
# 
# write_out(startrow)
