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
    teile = re.compile(r'(^\D)\s(\D*)(\d*$)')
    for i in ma_list:
        try:
            standort = teile.match(i).group(1).strip()
            kuerzel = teile.match(i).group(2).strip()
            id_num = int(teile.match(i).group(3).strip())
            print ("Agent: " + str(kuerzel) + " ist am Standort " + str(standort) + " und hat die Nummer " + str(id_num))
            agent_id_set[id_num] = dict()
            agent_id_set[id_num]["standort"] = standort
            agent_id_set[id_num]["kuerzel"] = kuerzel
        except:
            print("sth wrong with " + str(i))
    return agent_id_set

##########################################################################
##############START OF PROGRAM############################################
##########################################################################

agent_ids=dict()

agent_ids = get_cw_ma(sys.argv[1], agent_ids)
print agent_ids

agent_ids = get_cw_ma(sys.argv[2], agent_ids)
print agent_ids.items()
