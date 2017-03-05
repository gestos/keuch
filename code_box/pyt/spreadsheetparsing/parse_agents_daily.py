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


def get_rows_of_a_file(daily_file):
    sheet = xlrd.open_workbook(daily_file, formatting_info=True).sheet_by_index(0)
    rows_start = 4
    rows_end = sheet.nrows
    for i in range(rows_start,rows_end-1):
        stamp = sheet.cell(i,0).value
        date_object=parsedate_full(stamp)
        calweek = date_object.isocalendar()[1]
        print date_object,
        print "calendar week: ",
        print calweek,
        print date_object.year,
        print date_object.month,
        print date_object.day,
        print date_object.hour
    #date_of_sheet = parsedate(sheet.cell(1,1).value)
    #print date_of_sheet


##########################################################################
##############START OF PROGRAM############################################
##########################################################################

# agent_ids needs to be passed as a parameter and on return will be updated with new entries if they don't already exist
# will be updated for every file / every run
agent_ids=dict()
agent_ids = get_cw_ma(sys.argv[1], agent_ids)
agent_ids = get_cw_ma(sys.argv[2], agent_ids)

get_rows_of_a_file(sys.argv[1])
