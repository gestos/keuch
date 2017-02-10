#!/usr/bin/python
import os
import csv
import xlrd
import re
import sys
from natsort import natsorted, ns
import xlwt
from xlwt import Formula
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
        return xlspath, targetfile
# global variables for later use
neue_global = {}    # a dictionary of all files that aren't present in the target spreadsheet yet
neue_daten = []     # a list, only used for checking duplicates on the fly in the read_single_to_dict() function
dupes_global = {}       # a dictionary that contains list of files for duplicate dates
dupes_filelist = []     # a list of duplicate files that is referenced by the date key in dupes_global
agenten = {}
agenten_daten = []
other_global = {}       # a dictionary that contains files that aren't daily reports

xlspath, targetfile = check_cmdline_params()              # check for matching input / output files
wholdir = natsorted(os.listdir(xlspath), alg=ns.IGNORECASE, reverse=True)  # the list of all files in the specified directory

def parsedate(daily_sheet): # turn crap date into nice date
    date_crap = daily_sheet.cell(1,1).value # comes like this from upstream, date always lives at 1,1
    date_clea = re.sub(r' ', '.', date_crap[:10]) # transform to a string that strptime can parse
    date_objt = datetime.strptime(date_clea, "%d.%m.%Y").date() # this is a python datetime.date object
    xlint = (date_objt - date(1899, 12, 30)).days # this is an integer that excel uses internally
    return date_objt, xlint

def read_single_to_dict(single_xls_file):   # this func will determine what kind of file it has been passed (a report or something else), find out if it's a duplicate or unique and return a list of values depending on the file type
    input_sheet = xlrd.open_workbook(single_xls_file, formatting_info=True).sheet_by_index(0)
    rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
    global neue_daten
    uniqs = []
    dupes = []
    agnts = []
    other = []
    identifier = input_sheet.cell(0,0).value

    if identifier == "Hotlineber1458Gesing taegl":      # this would be a daily report of times and number of calls
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

    elif identifier == "Carexpert_Agent_Gesing":        # this would be a sheet for all agents with individual times
        agnts.append("a")
        agnts.append(single_xls_file)
        return agnts

    else:
        other.append("o")
        other.append(single_xls_file)
        return other

def read_date_from_target():
    target_xls = sys.argv[2]
    target_sheet = xlrd.open_workbook(target_xls).sheet_by_index(0)
    days_already = list()
    for i in target_sheet.col(0):
        if i.ctype == 3:
            days_already.append(i.value)
    return days_already

for item in wholdir:                    # iterates over every file in directory and returns a dictionary of 'duplicates', 'uniqes' with values and others
    if item.endswith('xls'):
        fullp_item = os.path.join(xlspath, item)
        file_examined = read_single_to_dict(fullp_item)                 # read_single_to_dict() returns a list (not a tuple or dict)
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
        elif file_examined[0] == "a":
            agenten.update({fullp_item: file_examined[1:]})
            agenten_daten.append(file_examined[1])
        elif file_examined[0] == "o":
            other_global.update({fullp_item: file_examined[1:]})
        else:
            print("huh? not a file format I can work with " + str(fullp_item))

# print("total files in this directory: " + str(len(wholdir)))
# print("dictionary of dupes\t\t\t"),
# print(dupes_global)
# print("dictionary of new uniques\t\t\t"),
# print(neue_global)

#print('liste aller doppelten: '),
#for k in sorted(dupes_global):
#    print(str(k) + " | " + str(dupes_global[k]))

#print('liste aller neuen:')
#for k in sorted(neue_global, key=lambda k: neue_global[k][0]): #this actually sorts by the first entry of the list (k)'s first item, which is the date integer
#    input_sheet = xlrd.open_workbook(k).sheet_by_index(0)
#    datu, integ = parsedate(input_sheet)
#    print(datu),
#    print(str(k) + "\t | \t" + str(neue_global[k]))

###############################
#### END READ, BEGIN WRITE ####
###############################

target_workbook = xlrd.open_workbook(targetfile, formatting_info=True)
target_workbook_writeable = xlcopy.copy(target_workbook)
targetsheet = target_workbook.sheet_by_index(0)
sheet_rw = target_workbook_writeable.get_sheet(0)
start_writing = targetsheet.nrows
new_entries_by_date = sorted(neue_global, key=lambda k: neue_global[k][0]) #this actually sorts by the first entry of the list (k)'s first item, which is the date integer
style_zahl_int = xlwt.easyxf('alignment: horiz centre')
style_datum = xlwt.easyxf('alignment: horiz centre; borders: right medium', num_format_str = "nn, dd.mm.yy")
style_stunden = xlwt.easyxf('alignment: horiz centre', num_format_str = "HH:MM:SS")

print(grn + "vorhandene Zeilen in Zieldatei:\t\t" + rst + str(start_writing-1) + ", ab " + str(start_writing) + " wird weitergeschrieben")

def write_out(startrow):
    ask = raw_input("do you really want that? [y/n]")[:1]
    if not ask.lower() == 'y':
        print("ok; bye :-)")
        exit()
    else:
        for row in new_entries_by_date:
            # idx = 0
            # for col in neue_global[row]:    # go through each column of the data set
            #     if idx == 0:    #0 ist das Datum wanted_cols = [3,21,5,12] # 3=telefonierte anrufe, 21=verlorene, 5=gesamtverbindungszeit 12=gesamtNBzeit
            #         sheet_rw.write(startrow, idx, col, style_datum)
            #     elif idx in (1, 2): # 1,2 = spalten 3, 21 im urpsrungssheet = telefonierte und verlorene. Format sollte Integer sein
            #         sheet_rw.write(startrow, idx, col)
            #     elif idx in (3, 4): # 3,4 = spalten 5, 12 im ursprunssheet = gesamtVBzeit und gesamtNBzeit. Format sollte HH:MM:SS sein (es geht jeweils nur um einen Tag, 24 HH sind ausreichend)
            #         sheet_rw.write(startrow, idx, col, style_stunden)
            #     idx += 1
            dat = neue_global[row][0] # Datum
            tel = neue_global[row][1] # Telefoniert
            ver = neue_global[row][2] # Verloren
            ges = neue_global[row][3] # Gespraechszeit
            nac = neue_global[row][4] # Nacharbeitszeit
            tot = ges+nac # Gesamtzeit

            sheet_rw.write(startrow, 0, dat, style_datum)   #Datum
            sheet_rw.write(startrow, 1, tel, style_zahl_int)    #Calls
            sheet_rw.write(startrow, 2, Formula("IF(%s=0,0,%s/%s)" % (tel, tot, tel)), style_stunden) 
            sheet_rw.write(startrow, 3, Formula("IF(%s=0,0,%s/%s)" % (tel, ges, tel)), style_stunden)
            sheet_rw.write(startrow, 4, Formula("IF(%s=0,0,%s/%s)" % (tel, nac, tel)), style_stunden)
            startrow += 1
        target_workbook_writeable.save(targetfile)
        # print(dir(xlrd))
        # print(targetsheet.cell(0,0).ctype)
        # print(targetsheet.cell(0,0).dump)
        # print("data written to " + targetfile)

write_out(start_writing)
# xlrd can't get the values of formula cells because those are only created when the file was saved (with "recalculate" option) in excel (or LO)
# so cells with formulas always return value "0.0" until they've been saved locally
