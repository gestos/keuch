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

def check_cmdline_params():
    global xlspath
    global targetfile
    if len(sys.argv) != 3:
        print("parseity need two parameters in the following order: $DIR where xls files lie and an xls $FILE to write into.")
        exit()
    elif not os.path.isdir(sys.argv[1]):
        print(sys.argv[1] + " is not a directory")
        exit()
    elif not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + " is not a regular file")
        exit()
    else:
        xlspath = os.path.abspath(sys.argv[1])
        targetfile = os.path.abspath(sys.argv[2])
        print("source:\t" + xlspath)
        print("target:\t" + targetfile)

check_cmdline_params()


def read_data_from_whole_dir():
    datensaetze_aller_files = list()
    for item in natsorted(os.listdir(xlspath), alg=ns.IGNORECASE, reverse=True):
        if item.endswith(".xls"):
            tabelle = os.path.join(xlspath, item)
            sheet0 = xlrd.open_workbook(tabelle).sheet_by_index(0)
            zeilen = sheet0.nrows

            Datum_B2 = sheet0.cell(1,1).value
            Datum_korrekt = re.sub(r' ', '.', Datum_B2[:10])
            Date_usable = datetime.strptime(Datum_korrekt, "%d.%m.%Y")
            
            wanted_cols = [2,3,4,5,12] # this is a comment 2=alle anrufe 3=telefonierte anrufe 4=gesamtanrufzeit 5=gesamtverbindungszeit 12=gesamtNBzeit
            sheet_data = list()
            sheet_data.append(Date_usable)
            for col in wanted_cols:
                col_total = float()
                for row in range(4,28):
                    cellvalue = sheet0.cell(row,col).value
                    col_total = col_total+cellvalue
                sheet_data.append(col_total)
            datensaetze_aller_files.append(sheet_data)
    return datensaetze_aller_files

#### END READ, BEGIN WRITE ####

target_workbook = xlrd.open_workbook(targetfile)
targetsheet = target_workbook.sheet_by_index(0)
schon_befueelt = targetsheet.nrows
row_to_write_in = schon_befueelt +1
target_workbook_writeable = xlcopy.copy(target_workbook)
sheet_rw = target_workbook_writeable.get_sheet(0)
all_data_from_dir = read_data_from_whole_dir()

print(grn + "vorhandene Zeilen in Zieldatei:\t\t" + rst + str(schon_befueelt) + ", ab " + str(row_to_write_in) + " wird weitergeschrieben")
print (grn + "Datenformat:\t\t\t\t" + rst + ", ".join(str(p) for p in all_data_from_dir[0])) # This shows that the list from above is still populated and available even outside the for loop
print("collected " + str(len(all_data_from_dir)) + " days of data")

#for single_day in sorted(all_data_from_dir):
#    print(single_day)


def write_out():
    start_writing = row_to_write_in
    style_datum = xlwt.easyxf(num_format_str = "nn, dd.mm.yy")
    style_stunden = xlwt.easyxf(num_format_str = "HH:MM:SS")
    yn = raw_input("do you really want that? [y/n]")[:1]
    if not yn.lower() == 'y':
        print("ok; bye :-)")
        exit()
    else:
        for einzelner_datensatz in sorted(all_data_from_dir):
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
        print("data written to " + targetfile)

write_out()
# xlrd can't get the values of formula cells because those are only created when the file was saved (with "recalculate" option) in excel (or LO)
# so cells with formulas always return value "0.0" until they've been saved locally
