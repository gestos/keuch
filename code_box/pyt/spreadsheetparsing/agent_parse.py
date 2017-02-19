#!/usr/bin/python
import os
import csv
import math
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

agentsfile = sys.argv[1]
input_sheet = xlrd.open_workbook(agentsfile, formatting_info=True).sheet_by_index(0)
rows_read, cols_read = input_sheet.nrows, input_sheet.ncols

col_timestamp = 0
col_agentname = 1
col_angenomme = 4
col_abgebroch = 22
col_bearbeitu = 24
col_verbindun = 29

startrow = 4            #die ersten 4 sind der fixe header, Daten beginnen bei Reihe 5 (in xlrd mit index 0 = 4)
endrow = rows_read-1    #letzte Reihe ist eine "Summe"-Reihe, Daten enden eine Reihe darueber



def get_uniq_agents():
    ag_ids = set()
    for i in range(startrow,endrow):
        ag_id = str(input_sheet.cell(i,col_agentname).value)
        ag_ids.add(ag_id)
    return ag_ids

vorhandene_agenten = get_uniq_agents()
ag_dic = {}

for i in vorhandene_agenten:
    agent_kuerzel = i[2:9]
    agent_standor = i[0]
    ag_dic[agent_kuerzel] = {}
    ag_dic[agent_kuerzel]["standort"] = agent_standor

def parseminutes(cellstring): # turn crap time into nice hh:mm:ss
    dec_s,minute = math.modf(cellstring)
    seconds= round(((dec_s*60)/100),2)
    zeit=minute+seconds
    date_objt = datetime.strptime(str(zeit), "%M.%S").time() # this is a python datetime.date object
    return date_objt

for ag in ag_dic:
    for i in range(startrow,endrow):
        if ag in input_sheet.cell(i,1).value:
            print("Agent: " + str(ag)),
            print("Ort: " + ag_dic[ag]["standort"]),
            print("Datum: " + str(input_sheet.cell(i,0).value)),
            print("angenommen: " + str(input_sheet.cell(i,4).value)),
            print("abgebrochen: " + str(input_sheet.cell(i,22).value)),
            bearbeitung = input_sheet.cell(i,24).value
            verbindung  = input_sheet.cell(i,29).value
            nacharbeit  = bearbeitung - verbindung
            print("Gesamt: " + str(parseminutes(bearbeitung))),
            print("Verbindung: " + str(parseminutes(verbindung))),
            print("Nacharbeit: " + str(parseminutes(nacharbeit)))

    print("end of agent dataset "+ str(ag))
    print


#
#
#
#
#
#
#
#
#
# # todo: clean up directory of badly named xls files
# # for file_in_path:
# #     check timestamp
# #     if timestamp is in multiple files:
# #         compare files (maybe checksum md5 or something?)
# #         if files are identical:
# #             keep only one, delete others
# #         else:
# #             print filenames and message: please clean up this mess
#
# def check_cmdline_params():
#     if len(sys.argv) != 3:
#         print(sys.argv[0] +" needs two parameters in the following order: $DIR where xls files lie and an xls $FILE to write into.")
#         exit()
#     elif not os.path.isdir(sys.argv[1]):
#         print(sys.argv[1] + " is not a directory")
#         exit()
#     elif not os.path.isfile(sys.argv[2]):
#         print(sys.argv[2] + " is not a regular file")
#         exit()
#     else:
#         xlspath = os.path.abspath(sys.argv[1])
#         targetfile = os.path.abspath(sys.argv[2])
#         print("source:\t" + xlspath)
#         print("target:\t" + targetfile)
#         return xlspath, targetfile
# # global variables for later use
# neue_global = {}    # a dictionary of all files that aren't present in the target spreadsheet yet
# neue_daten = []     # a list, only used for checking duplicates on the fly in the read_single_to_dict() function
# dupes_global = {}       # a dictionary that contains list of files for duplicate dates
# dupes_filelist = []     # a list of duplicate files that is referenced by the date key in dupes_global
# agenten = {}            # a dictionary of files that are "monthly" stats for each single agent
# agenten_daten = []      # a list of filenames of that dict
# other_global = {}       # a dictionary that contains files that aren't daily reports
#
# xlspath, targetfile = check_cmdline_params()              # check for matching input / output files
# wholdir = natsorted(os.listdir(xlspath), alg=ns.IGNORECASE, reverse=True)  # the list of all files in the specified directory
#
# def parsedate(daily_sheet): # turn crap date into nice date
#     date_crap = daily_sheet.cell(1,1).value # comes like this from upstream, date always lives at 1,1
#     date_clea = re.sub(r' ', '.', date_crap[:10]) # transform to a string that strptime can parse
#     date_objt = datetime.strptime(date_clea, "%d.%m.%Y").date() # this is a python datetime.date object
#     xlint = (date_objt - date(1899, 12, 30)).days # this is an integer that excel uses internally
#     return date_objt, xlint
#
# def read_single_to_dict(single_xls_file):   # this func will determine what kind of file it has been passed (a report or something else), find out if it's a duplicate or unique and return a list of values depending on the file type
#     input_sheet = xlrd.open_workbook(single_xls_file, formatting_info=True).sheet_by_index(0)
#     rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
#     global neue_daten
#     uniqs = []
#     dupes = []
#     agnts = []
#     other = []
#     identifier = input_sheet.cell(0,0).value
#
#     if identifier == "Hotlineber1458Gesing taegl":      # this would be a daily report of times and number of calls
#         datum = parsedate(input_sheet)[0] # useable date
#         xlint = parsedate(input_sheet)[1] # excel date float
#         if (xlint in read_date_from_target() or xlint in neue_daten):       # if the date is somewhere in either the target file or the dictionary of new dates
#             dupes.extend(("d", datum, single_xls_file))                     # set a duplicate flag and return the date and full filepath
#             return dupes
#         else:                                                               # if the spreadsheet's date is unique, we want the following values:
#             wanted_cols = [3,21,5,12]                                       # 3=telefonierte anrufe, 21=verlorene, 5=gesamtverbindungszeit 12=gesamtNBzeit
#             uniqs.append("u")                                               # set a flag that this file is uniqe
#             uniqs.append(xlint)
#             for col in wanted_cols:                                 # calculate total for each wanted column (this is already a confirmed daily report, so we can do this)
#                 col_total = float()
#                 for row in range(4,27):
#                     cellvalue = input_sheet.cell(row,col).value
#                     col_total = col_total+cellvalue
#                 uniqs.append(col_total)                             # append the total of each column to the list; list will be [flag, date, col3, col5, col12, col21]
#             return uniqs
#
#     elif identifier == "Carexpert_Agent_Gesing":        # this would be a sheet for all agents with individual times
#         agnts.append("a")
#         agnts.append(single_xls_file)
#         return agnts
#
#     else:
#         other.append("o")
#         other.append(single_xls_file)
#         return other
#
# def read_date_from_target():
#     target_xls = sys.argv[2]
#     target_sheet = xlrd.open_workbook(target_xls).sheet_by_index(0)
#     days_already = list()
#     for i in target_sheet.col(0):
#         if i.ctype == 3:
#             days_already.append(i.value)
#     return days_already
#
# for item in wholdir:                    # iterates over every file in directory and returns a dictionary of 'duplicates', 'uniqes' with values and others
#     if item.endswith('xls'):
#         fullp_item = os.path.join(xlspath, item)
#         file_examined = read_single_to_dict(fullp_item)                 # read_single_to_dict() returns a list (not a tuple or dict)
#         if file_examined[0] == "d":                                     # file_examined[0] = flag, ob doppel oder nicht
#             dupes_filelist=[]                                           # fuer jeden durchgang soll die Liste erst mal leer sein
#             if file_examined[1] in dupes_global:                               # file_examined[1] = Datum(sobjekt)
#                 dupes_global[file_examined[1]].append(file_examined[2])        # file_examined[2] = pfad zur Datei
#             else:
#                 dupes_filelist.append(file_examined[2])
#                 dupes_global.update({file_examined[1]: dupes_filelist})
#         elif file_examined[0] == "u":
#             neue_global.update({fullp_item: file_examined[1:]})
#             neue_daten.append(file_examined[1])
#         elif file_examined[0] == "a":
#             agenten.update({fullp_item: file_examined[1:]})
#             agenten_daten.append(file_examined[1])
#         elif file_examined[0] == "o":
#             other_global.update({fullp_item: file_examined[1:]})
#         else:
#             print("huh? not a file format I can work with " + str(fullp_item))
#
# ###############################
# #### END READ, BEGIN WRITE ####
# ###############################
#
# target_workbook = xlrd.open_workbook(targetfile, formatting_info=True)
# target_workbook_writeable = xlcopy.copy(target_workbook)
# targetsheet = target_workbook.sheet_by_index(0)
# sheet_rw = target_workbook_writeable.get_sheet(0)
# start_writing = targetsheet.nrows
# new_entries_by_date = sorted(neue_global, key=lambda k: neue_global[k][0]) #this actually sorts by the first entry of the list (k)'s first item, which is the date integer; this will return a list of filenames
#
# style_calls             = xlwt.easyxf('alignment: horiz centre')
# style_verlo             = xlwt.easyxf('alignment: horiz centre; font: color gray25')
# style_datum             = xlwt.easyxf('alignment: horiz right; borders: right double, right_color 0x28, left double, left_color 0x28', num_format_str = "ddd dd.mm.yy")
# style_minuten           = xlwt.easyxf('alignment: horiz centre', num_format_str = "HH:MM:SS")
# style_minuten_gesamt    = xlwt.easyxf('alignment: horiz centre; borders: right double, right_color 0x28, left double, left_color 0x28; pattern: pattern solid, fore_color ice_blue', num_format_str = "HH:MM:SS")
#
# print(grn + "vorhandene Zeilen in Zieldatei:\t\t" + rst + str(start_writing-1) + ", ab " + str(start_writing) + " wird weitergeschrieben")
#
# def write_out(startrow):
#     print(str(len(new_entries_by_date)) + " days that aren't already listed")
#     ask = raw_input("do you really want that? [y/n]")[:1]
#     if not ask.lower() == 'y':
#         print("ok; bye :-)")
#         exit()
#     else:
#         for row in new_entries_by_date:
#             dat = neue_global[row][0] # Datum
#             tel = neue_global[row][1] # Telefoniert
#             ver = neue_global[row][2] # Verloren
#             ges = neue_global[row][3] # Gespraechszeit
#             nac = neue_global[row][4] # Nacharbeitszeit
#             tot = ges+nac # Gesamtzeit
#
#             sheet_rw.write(startrow, 0, dat, style_datum)   #Datum
#             sheet_rw.write(startrow, 1, tel, style_calls)    #Calls
#             sheet_rw.write(startrow, 2, Formula("IF(%s=0,0,%s/%s)" % (tel, ges, tel)), style_minuten) # av. total
#             sheet_rw.write(startrow, 3, Formula("IF(%s=0,0,%s/%s)" % (tel, nac, tel)), style_minuten) # av. talk
#             sheet_rw.write(startrow, 4, Formula("IF(%s=0,0,%s/%s)" % (tel, tot, tel)), style_minuten_gesamt) # av. after
#             sheet_rw.write(startrow, 6, ver, style_verlo) # Verlorene
#             startrow += 1
#         target_workbook_writeable.save(targetfile)
#
# write_out(start_writing)
#
# # print("dude, there's still" + str(agenten) + " to be parsed")
# # xlrd can't get the values of formula cells because those are only created when the file was saved (with "recalculate" option) in excel (or LO)
# # so cells with formulas always return value "0.0" until they've been saved locally
