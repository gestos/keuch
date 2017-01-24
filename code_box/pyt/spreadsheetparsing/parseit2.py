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
from datetime import date

# define some colors for output later
grn = coly.GREEN
blu = coly.BLUE
cya = coly.CYAN
red = coly.RED
rst = coln.RESET_ALL

# todo: clean up directory of badly named xls files
# for file_in_path:
#     check timestamp
#     if timestamp is in multiple files:
#         compare files (maybe checksum md5 or something?)
#         if files are identical:
#             keep only one, delete others
#         else:
#             print filenames and message: please clean up this mess

def check_cmdline_params():
    global xlspath
    global targetfile
    if len(sys.argv) != 3:
        print(sys.argv[0] +" needs two parameters in the following order: $DIR where xls files lie and an xls $FILE to write into.")
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


def parsedate(daily_sheet): # turn crap date into nice date
    date_crap = daily_sheet.cell(1,1).value # comes like this from upstream, date always lives at 1,1
    date_clea = re.sub(r' ', '.', date_crap[:10]) # transform to a string that strptime can parse
    date_objt = datetime.strptime(date_clea, "%d.%m.%Y").date() # this is a python datetime.date object
    xlint = (date_objt - date(1899, 12, 30)).days # this is an integer that excel uses internally
    return date_objt, xlint



def read_single_to_dict(single_xls_file):
    input_sheet = xlrd.open_workbook(single_xls_file).sheet_by_index(0)
    rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
    uniqs = []
    dupes = []
    other = []
    # print (str(single_xls_file[-13:]) + " has " + str(rows_read) + " rows and " + str(cols_read) + " cols"),

    if rows_read == 29 and cols_read == 23: # this is a daily report that we want to read from
        datum = parsedate(input_sheet)[0] # useable date
        xlint = parsedate(input_sheet)[1] # excel date float

        if xlint in read_date_from_target():
            dupes.extend(("d", datum, single_xls_file))
            return dupes
            print(str(single_xls_file[-13:]) + ' is a daily report for ' + str(datum) + "(" + str(xlint) + ")")
            print ("xlint is already in date list")
        else:
            #print(str(single_xls_file[-13:]) + ' is a daily report for ' + str(datum) + "(" + str(xlint) + ")")
            wanted_cols = [3,21,5,12] # 3=telefonierte anrufe, 21=verlorene, 5=gesamtverbindungszeit 12=gesamtNBzeit
            wanted_colsd = {3: 'verbundene' ,21: 'verlorene', 5: 'verbindungszeit', 12: 'nacharbeitszeit'} # 3=telefonierte anrufe, 21=verlorene, 5=gesamtverbindungszeit 12=gesamtNBzeit
            uniqs.append("u")
            uniqs.append(xlint)
            for col in wanted_cols:
                col_total = float()
                #print(wanted_colsd[col]),
                for row in range(4,27):
                    cellvalue = input_sheet.cell(row,col).value
                    col_total = col_total+cellvalue
                uniqs.append(col_total)
                #print(col_total),
            return uniqs
    else:
        other.append(single_xls_file)
        return other




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

            wanted_cols = [2,3,4,5,12] # 2=alle anrufe 3=telefonierte anrufe 4=gesamtanrufzeit 5=gesamtverbindungszeit 12=gesamtNBzeit
            uniqs = list()
            uniqs.append(Date_usable)
            for col in wanted_cols:
                col_total = float()
                for row in range(4,28):
                    cellvalue = sheet0.cell(row,col).value
                    col_total = col_total+cellvalue
                uniqs.append(col_total)
            datensaetze_aller_files.append(uniqs)
    return datensaetze_aller_files




def read_date_from_target():
    target_xls = sys.argv[2]
    target_sheet = xlrd.open_workbook(target_xls).sheet_by_index(0)
    days_already = list()
    for i in target_sheet.col(0):
        if i.ctype == 3:
            days_already.append(i.value)
    return days_already

# read_single_to_dict()

neue = {}
dupes = {}
neue1 = {}
dupes1 = {}
dupes1_reslist = list()

### Schluessel/Wert mue andersum sein. Output der Duplikate sollte "20.01.2017" : [file1, file2, file2] sein....
### wohl am besten dictionary of lists
for item in natsorted(os.listdir(xlspath), alg=ns.IGNORECASE, reverse=True):
    fullp_item = os.path.join(xlspath, item)
    file_examined = read_single_to_dict(fullp_item)
    print (str(fullp_item) + ": " + str(type(file_examined)))
    if file_examined[0] == "d":
        print("is a dupe")
    elif file_examined[0] == "u":
        print("is a new entry")
    elif file_examined[0] == None:
        print("???" + str(fullp_item))
    else:
        print("huh?")

print(file_examined)






















#### END READ, BEGIN WRITE ####

#target_workbook = xlrd.open_workbook(targetfile)
#targetsheet = target_workbook.sheet_by_index(0)
#schon_befueelt = targetsheet.nrows
#row_to_write_in = schon_befueelt +1
#target_workbook_writeable = xlcopy.copy(target_workbook)
#sheet_rw = target_workbook_writeable.get_sheet(0)
# all_data_from_dir = read_data_from_whole_dir()

# print(grn + "vorhandene Zeilen in Zieldatei:\t\t" + rst + str(schon_befueelt) + ", ab " + str(row_to_write_in) + " wird weitergeschrieben")
# print (grn + "Datenformat:\t\t\t\t" + rst + ", ".join(str(p) for p in all_data_from_dir[0])) # This shows that the list from above is still populated and available even outside the for loop
# print("collected " + str(len(all_data_from_dir)) + " days of data")

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

# write_out()
# xlrd can't get the values of formula cells because those are only created when the file was saved (with "recalculate" option) in excel (or LO)
# so cells with formulas always return value "0.0" until they've been saved locally
