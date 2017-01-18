#!/usr/bin/python
import os
import csv
import xlrd
import re
import sys
from natsort import natsorted, ns
import xlwt
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import datetime

grn = coly.GREEN
blu = coly.BLUE
cya = coly.CYAN
red = coly.RED
rst = coln.RESET_ALL

def check_xls_path():
    if len(sys.argv) > 1:
        xlspath = os.path.abspath(sys.argv[1])
    else:
        xlspath = '/home/keuch/gits/wiki_carex/stats/Hotlineber1458Gesing_taegl_217_HOURLY/'
    print (grn + "Directory with .xls files is set to:\t" + rst + xlspath)
    return xlspath

daily_report_dir_path = check_xls_path()

def read_data_from_whole_dir():
    datensaetze_aller_files = list()
    for tabelle in natsorted(os.listdir(daily_report_dir_path), alg=ns.IGNORECASE, reverse=True):
        if tabelle.endswith(".xls"):
            tabelle_fullpath = os.path.join(daily_report_dir_path, tabelle)
            ganze_tabelle = xlrd.open_workbook(tabelle_fullpath)
            erstes_sheet = ganze_tabelle.sheet_by_index(0)
            zeilen = erstes_sheet.nrows
            Datum_B2 = erstes_sheet.cell(1,1).value
            Datum_korrekt = re.sub(r' ', '.', Datum_B2[:10]) 
            Date_usable = datetime.strptime(Datum_korrekt, "%d.%m.%Y")
            wanted_cols = [2,3,4,5,12] # this is a comment 2=alle anrufe 3=telefonierte anrufe 4=gesamtanrufzeit 5=gesamtverbindungszeit 12=gesamtNBzeit
            datensatz_fuer_dieses_sheet = list()
            datensatz_fuer_dieses_sheet.append(Date_usable)
            for Spalte in wanted_cols:
                summe = float() 
                for summenreihen in range(4,28):
                    summand = erstes_sheet.cell(summenreihen,Spalte).value
                    summe = summe+summand
                datensatz_fuer_dieses_sheet.append(summe)
            datensaetze_aller_files.append(datensatz_fuer_dieses_sheet)
    return datensaetze_aller_files

#### END READER ####


#### BEGIN WRITER ####

targetfile = '/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/target.xls'
target_workbook = xlrd.open_workbook(targetfile)
sheets_in_targetfile = target_workbook.sheet_names()
targetsheet = target_workbook.sheet_by_index(0)
schon_befueelt = targetsheet.nrows
row_to_write_in = schon_befueelt +1
target_workbook_writeable = xlcopy.copy(target_workbook)
sheet_rw = target_workbook_writeable.get_sheet(0)
liste_aller_gelesenen_files = read_data_from_whole_dir()

print (grn + "Zieldatei hat folgende Sheets:\t\t" + rst + ",".join(sheets_in_targetfile))
print(grn + "vorhandene Zeilen in Zieldatei:\t\t" + rst + str(schon_befueelt) + ", ab " + str(row_to_write_in) + " wird weitergeschrieben")
print (grn + "Datenformat:\t\t\t\t" + rst + ", ".join(str(p) for p in liste_aller_gelesenen_files[0])) # This shows that the list from above is still populated and available even outside the for loop


for tag in sorted(liste_aller_gelesenen_files):
    print(tag)


def write_out():
    start_writing = row_to_write_in
    style_datum = xlwt.easyxf(num_format_str = "nn, dd.mm.yy")
    style_stunden = xlwt.easyxf(num_format_str = "HH:MM:SS")
    for einzelner_datensatz in sorted(liste_aller_gelesenen_files):
        idx = 0
        for spalte_eines_datensatzes in einzelner_datensatz:
            if idx == 0:
                sheet_rw.write(start_writing, idx, spalte_eines_datensatzes, style_datum)
            elif idx in (1, 2):
                sheet_rw.write(start_writing, idx, spalte_eines_datensatzes)
            elif idx in (3, 4, 5):
                sheet_rw.write(start_writing, idx, spalte_eines_datensatzes, style_stunden)
            idx += 1
        start_writing += 1
    target_workbook_writeable.save(targetfile)

write_out()
# xlrd can't get the values of formula cells because those are only created when the file was saved (with "recalculate" option) in excel (or LO)
# so cells with formulas always return value "0.0" until they've been saved locally
