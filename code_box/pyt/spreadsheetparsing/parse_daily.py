#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import datetime,date

def get_cw_ma(ma_file, agent_id_set):
    ma_cell = xlrd.open_workbook(ma_file, formatting_info=True).sheet_by_index(0).cell(0,1).value
    ma_list = ma_cell.split(',')
    teile = re.compile(r'(^\D)\s(.*)(\b\d[\d\s]*$)')
    for i in ma_list:
        try:
	    standort = teile.match(i).group(1).strip()
            kuerzel = teile.match(i).group(2).strip()
            id_num = int(teile.match(i).group(3).strip())
            if not id_num in agent_id_set:
                agent_id_set[id_num] = dict()
                agent_id_set[id_num]["standort"] = standort
                agent_id_set[id_num]["kuerzel"] = kuerzel
        except:
            print("sth wrong with " + str(i))
    return agent_id_set

def parsedate_full(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell # comes like this from upstream, date always lives at 1,1
    day, mon, yea, hou, mnt = date_crap[1:3], date_crap[4:6], date_crap[7:11], date_crap[12:14], date_crap[15:17]
    date_clea=str(day+"."+mon+"."+yea+"."+hou)
    date_objt = datetime.strptime(date_clea, "%d.%m.%Y.%H") # this is a python datetime.date object
    return date_objt

def filerows_into_dict(daily_file,filldict,index_dict):
    sheet = xlrd.open_workbook(daily_file, formatting_info=True).sheet_by_index(0)
    rows_start = 4
    rows_end = sheet.nrows
    id_num = re.compile(r'.*\b(\d\d*)$')
    rowsofdict = len(filldict)  # we'll have an index of the overall rows
    for i in range(rows_start,rows_end-1):
        rowsofdict += 1
        timestamp = parsedate_full(sheet.cell(i,0).value) # this will be the dictionary key as it is the unique overall key
        filldict[rowsofdict] = {}
        filldict[rowsofdict]["timestamp"] = timestamp
        idnummer = int(id_num.match(sheet.cell(i,1).value).group(1).strip())
        filldict[rowsofdict]["bearbeiter"] = agent_ids[idnummer]
        filldict[rowsofdict]["calweek"] = timestamp.isocalendar()[1]
        filldict[rowsofdict]["weekday"] = timestamp.strftime("%a")
        filldict[rowsofdict]["year"] = timestamp.year
        filldict[rowsofdict]["month"] = timestamp.strftime("%b")
        filldict[rowsofdict]["day"] = timestamp.day
        filldict[rowsofdict]["hour"] = timestamp.hour
        if 11 <= timestamp.hour <=19:
            filldict[rowsofdict]["bzeit"] = "kern"
        else:
            filldict[rowsofdict]["bzeit"] = "neben"
        filldict[rowsofdict]["ang_anrufe"] = int(sheet.cell(i,4).value)
        filldict[rowsofdict]["gesamt"] = sheet.cell(i,24).value
        filldict[rowsofdict]["verbindung"] = sheet.cell(i,29).value

        index_dict["agents_actual"].add(idnummer)
        index_dict["weeks"].add(timestamp.isocalendar()[1])
        index_dict["years"].add(timestamp.year)
        index_dict["months"].add(timestamp.strftime("%b"))
        index_dict["days"].add(timestamp.day)

    return filldict, index_dict
#date_of_sheet = parsedate(sheet.cell(1,1).value)
#print date_of_sheet
##########################################################################
##############START OF PROGRAM############################################
##########################################################################
# agent_ids needs to be passed as a parameter and on return will be updated with new entries if they don't already exist
# will be updated for every file / every run
agent_ids=dict()
doe = dict()    # dict of everything
index_dict = dict()
index_dict["years"] = set()
index_dict["months"] = set()
index_dict["weeks"] = set()
index_dict["days"] = set()
index_dict["agents_actual"] = set()

agent_ids = get_cw_ma(sys.argv[1], agent_ids)

doe,index_dict = filerows_into_dict(sys.argv[1],doe,index_dict)

for day in index_dict["days"]:
    print day
    for entry in doe:
        if doe[entry]["day"] == day:
            print doe[entry]
