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
from collections import defaultdict
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

def read_single_to_dict(single_xls_file):   # this func will determine what kind of file it has been passed (a report or something else), find out if it's a duplicate or unique and return a list of values depending on the file type
    input_sheet = xlrd.open_workbook(single_xls_file).sheet_by_index(0)
    rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
    global neue_daten
    uniqs = []
    dupes = []
    other = []
    identifier = input_sheet.cell(0,0).value

    if identifier == "Hotlineber1458Gesing taegl":
        datum = parsedate(input_sheet)[0] # useable date
        xlint = parsedate(input_sheet)[1] # excel date float

        if (xlint in read_date_from_target() or xlint in neue_daten):       # if the date is somewhere in either the target file or the dictionary of new dates
            dupes.extend(("d", datum, single_xls_file))                     # set a duplicate flag and return the date and full filepath
            return dupes
        else:                                                               # if the spreadsheet's date is unique, we want the following values:
            wanted_cols = [3,21,5,12]                                       # 3=telefonierte anrufe, 21=verlorene, 5=gesamtverbindungszeit 12=gesamtNBzeit
            uniqs.append("u")                                               # set a flag that this file is uniqe
            uniqs.append(xlint)                                             
            for col in wanted_cols:                                 # calculate total for each wanted column (this is already a confirmed daily report, so we can do this)
                col_total = float()
                for row in range(4,27):
                    cellvalue = input_sheet.cell(row,col).value
                    col_total = col_total+cellvalue
                uniqs.append(col_total)                             # append the total of each column to the list; list will be [flag, date, col3, col5, col12, col21]
            return uniqs
    else:
        other.append("o")
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

neue_global = {}    # a dictionary of all files that aren't present in the target spreadsheet yet
neue_daten = []     # a list, only used for checking duplicates on the fly in the read_single_to_dict() function
dupes_global = {}       # a dictionary that contains list of files for duplicate dates
dupes_filelist = []     # a list of duplicate files that is referenced by the date key in dupes_global
other_global = {}       # a dictionary that contains files that aren't daily reports
wholdir = natsorted(os.listdir(xlspath), alg=ns.IGNORECASE, reverse=True)  # the list of all files in the specified directory

for item in wholdir:
    if item.endswith('xls'):
        fullp_item = os.path.join(xlspath, item)
        file_examined = read_single_to_dict(fullp_item)
        if file_examined[0] == "d":                                     # file_examined[0] = flag, ob doppel oder nicht
            dupes_filelist=[]                                           # fuer jeden durchgang soll die Liste erst mal leer sein
            if file_examined[1] in dupes_global:                               # file_examined[1] = Datum(sobjekt)
                dupes_global[file_examined[1]].append(file_examined[2])        # file_examined[2] = pfad zur Datei
            else:
                dupes_filelist.append(file_examined[2])
                dupes_global.update({file_examined[1]: dupes_filelist})
        elif file_examined[0] == "u":
            neue_global.update({fullp_item: file_examined[1:]})
            neue_daten.append(file_examined[1])
        elif file_examined[0] == "o":
            other_global.update({fullp_item: file_examined[1:]})
        else:
            print("huh?")

print("total files in this directory: " + str(len(wholdir)))
print("dictionary of dupes\t\t\t"),
print(dupes_global)
print("dictionary of new uniques\t\t\t"),
print(neue_global)

#print('liste aller doppelten: '),
#for k in sorted(dupes_global):
#    print(str(k) + " | " + str(dupes_global[k]))


########### Duplicates are parsed correctly, but new entries fail to check for dupes on the fly
########### solution a) write after each row and save. date will be in file an will be read
########### solution b) check while parsing... hm

print('liste aller neuen: ')
for k in sorted(neue_global, key=lambda k: neue_global[k][0]): #this actually sorts by the first entry of the list (k)'s first item, which is the date integer
    input_sheet = xlrd.open_workbook(k).sheet_by_index(0)
    datu, integ = parsedate(input_sheet)
    print(datu),
    print(str(k) + " | " + str(neue_global[k]))

#print('andere xls, keine reports: ' + str(other_global))
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
