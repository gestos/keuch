#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import datetime,date



def get_cw_ma(ma_file):
    sheet = xlrd.open_workbook(ma_file, formatting_info=True).sheet_by_index(0)
    srow = 2
    erow = sheet.nrows
    col = 2
    mitarbeiter = dict()
    for row in range(srow, erow):
        if sheet.cell(row,2).value:
            print type(sheet.cell(row,2).value)
            print int(sheet.cell(row,2).value)
            int(sheet.cell(row,2).value)
        
        
##########################################################################
##############START OF PROGRAM############################################
##########################################################################

get_cw_ma(sys.argv[1])
