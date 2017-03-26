#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime

#We need:   a row for each day (day=datetime timestamp with year-month-day
#           a column for each hour
#           HALF hours... like 00:00 to 00:30, then 00:30 to 01:30 and finally 23:30 to 00:00


def check_cmdline_params():
    if len(sys.argv) != 3:
        print(sys.argv[0])
        print(textwrap.fill("1. Argument muss eine HOTLINEstatistik (nicht Agenten- oder Terminierungsstatistik) ODER ein Verzeichnis mit solchen sein. Diese muss viertelstuendlich aufgedroeselt sein, um eine Trennung nach Kern- und Nebenzeiten zu ermoeglichen.",80))
        print
        print(textwrap.fill("2. Argument ist die Ziel-Exceldatei, dorthin wird entweder die generierte Zeile unten eingefuegt, oder das gesamte Verzeichnis neu geschrieben",80))
        exit()
    elif not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " is not a regular file")
        exit()
    elif not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + " is not a regular file")
        exit()
    else:
        sourcefile_IB = os.path.abspath(sys.argv[1])
        targetfile = os.path.abspath(sys.argv[2])
        print("source inbound:\t" + sourcefile_IB)
        print("target:\t" + targetfile)
        return sourcefile_IB, targetfile

def parsedate_full(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea, hou, mnt = date_crap[0:2], date_crap[3:5], date_crap[6:10], date_crap[11:13], date_crap[14:16]
    date_clea=str(day+"."+mon+"."+yea+"."+hou+"."+mnt)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y.%H.%M") # this is a python datetime.date object
    return date_objt

def generate_single_day(source):
    #spalten: 0=timestamp 2=angenommen 3=verbunden 5=TT 12=ACW    // Lost = [2]-[3], HT = [5]+[12]
    sheet = xlrd.open_workbook(source, formatting_info=True).sheet_by_index(0)
    rows_start = 4
    rows_end = sheet.nrows
    datum = parsedate_full(sheet.cell(4,0).value).date() # this will be the dictionary key as it is the unique overall key
    calweek = datum.isocalendar()[1]
    startkern = datetime.time(11,30,00)
    endkern = datetime.time(19,30,00)
    hour_indices = dict()
    for i in range (0,25):
        hour_indices[i] = dict()
        hour_indices[i]["angekommen"] = 0
        hour_indices[i]["verbunden"] = 0
        hour_indices[i]["verloren"] = 0
        hour_indices[i]["servicelevel"] = 0
    hour_index = 0

    for i in range(rows_start,rows_end-1):
        timestamp = parsedate_full(sheet.cell(i,0).value)
        if 0 <= timestamp.minute <=29:
            hour_index = timestamp.hour
            hour_indices[hour_index]["angekommen"] += sheet.cell(i,2).value
            hour_indices[hour_index]["verbunden"] += sheet.cell(i,3).value
            hour_indices[hour_index]["verloren"] += (sheet.cell(i,2).value - sheet.cell(i,3).value)
        elif 30 <= timestamp.minute <=59:
            hour_index = timestamp.hour +1
            hour_indices[hour_index]["angekommen"] += sheet.cell(i,2).value
            hour_indices[hour_index]["verbunden"] += sheet.cell(i,3).value
            hour_indices[hour_index]["verloren"] += (sheet.cell(i,2).value - sheet.cell(i,3).value)

    for hour in hour_indices.keys():
        if hour_indices[hour]["verbunden"] > 0:
            hour_indices[hour]["servicelevel"] = (hour_indices[hour]["verbunden"] / hour_indices[hour]["angekommen"])
        else:
            if hour_indices[hour]["angekommen"] == 0:
                hour_indices[hour]["servicelevel"] = 1 
            elif hour_indices[hour]["angekommen"] > 0:
                hour_indices[hour]["servicelevel"] = 0 

    return datum, calweek, hour_indices


def write_out(in_dict,target_file):
    target_workbook     = xlrd.open_workbook(target_file, formatting_info=True)
    sheet_verbunden     = target_workbook.sheet_by_index(0)
    sheet_verloren      = target_workbook.sheet_by_index(1)
    sheet_sla           = target_workbook.sheet_by_index(2)
    row_verbunden       = sheet_verbunden.nrows
    row_verloren        = sheet_verloren.nrows
    row_sla             = sheet_sla.nrows
    target_workbook_writeable   = xlcopy.copy(target_workbook)
    sheet_verbunden_rw          = target_workbook_writeable.get_sheet(0)
    sheet_verloren_rw           = target_workbook_writeable.get_sheet(1)
    sheet_sla_rw                = target_workbook_writeable.get_sheet(2)

    style_datum             = xlwt.easyxf('alignment: horiz right; borders: right double, right_color 0x28, left double, left_color 0x28', num_format_str = "ddd, dd.mm.yy")
    style_conn           = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color 0x2c')
    style_n_conn           = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color 0x1f')
    style_sla               = xlwt.easyxf('alignment: horiz centre;', num_format_str = "0.00")

    sheet_verbunden_rw.write(row_verbunden, 0, tag, style_datum)   #Datum
    sheet_verloren_rw.write(row_verloren, 0, tag, style_datum)   #Datum
    sheet_sla_rw.write(row_sla, 0, tag, style_datum)   #Datum
    sheet_verbunden_rw.write(row_verbunden, 1, kw)   #Datum
    sheet_verloren_rw.write(row_verloren, 1, kw)   #Datum
    sheet_sla_rw.write(row_sla, 1, kw)   #Datum
    for index in in_dict:   # der Stunden_index faengt bei 0 an und ist analog zu den Spalten im Sheet
    
        conn  = in_dict[index]['verbunden']
        sheet_verbunden_rw.write(row_verbunden,index+2, conn, style_conn)

        n_conn  = in_dict[index]['verloren']
        sheet_verloren_rw.write(row_verloren,index+2,n_conn, style_n_conn)
    
        sla  = in_dict[index]['servicelevel']
        sheet_sla_rw.write(row_sla,index+2,sla, style_sla)
    target_workbook_writeable.save(target)

####################end of function definitions#####################

source,target = check_cmdline_params()

tag,kw,stunden = generate_single_day(source)

write_out(stunden,target)
