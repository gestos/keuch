#!/usr/bin/python
import os, csv, math, shutil, xlrd, re, sys, xlwt
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import datetime,date

def check_cmdline_params():
    if len(sys.argv) == 1:
        print ("Verwendung: entweder eine Datei oder einen ganzen Ordner als Parameter eingeben")
        print ("Programm sucht nach Excel-Dateien, identifiziert die Art des Reports und benennt die Datei anhand des vorgefundenen Datums um")
        exit()
    elif len(sys.argv) != 2:
        print(sys.argv[0] +" will take one argument: either a $DIR or a $FILE to process")
        exit()
    elif os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " is a regular file to be renamed")
        flag="single"
        return flag
    elif os.path.isdir(sys.argv[1]):
        print(sys.argv[1] + " is a directory to be processed")
        flag="multi"
        return flag
    else:
        print("neither file nor dir? exiting")
        exit()
flag=check_cmdline_params()

def parsedate(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    date_clea = re.sub(r' ', '.', date_crap[:10]) # transform to a string that strptime can parse
    date_objt = datetime.strptime(date_clea, "%d.%m.%Y").date() # this is a python datetime.date object
    xlint = (date_objt - date(1899, 12, 30)).days # this is an integer that excel uses internally
    calweek = date_objt.isocalendar()[1]
    return date_objt, xlint, calweek

def rename_xls(excelfile):
    directory,filename_only=(os.path.split(excelfile))
    extension=(os.path.splitext(filename_only)[1])

    def renamefile_kw(newprefix,KW=None):
        input_sheet = xlrd.open_workbook(excelfile, formatting_info=True).sheet_by_index(0)
        datecell = input_sheet.cell(1,1).value
        calweek = "%0*d" % (2, parsedate(datecell)[2]) # calendar week with a leading zero
        year = str(parsedate(datecell)[0]) # calendar week with a leading zero
        filenew=(newprefix+year[:4]+KW+str(calweek)+str(extension))
        euroFilename = os.path.join(directory,filenew)
        print('Renaming "%s" to "%s"...' % (excelfile, euroFilename))
        shutil.move(excelfile, euroFilename)   # uncomment after testing

    def renamefile(newprefix):
        input_sheet = xlrd.open_workbook(excelfile, formatting_info=True).sheet_by_index(0)
        datecell = input_sheet.cell(1,1).value
        date_day = str(parsedate(datecell)[0]) # calendar week with a leading zero
        filenew=(newprefix+date_day+str(extension))
        euroFilename = os.path.join(directory,filenew)
        print('Renaming "%s" to "%s"...' % (excelfile, euroFilename))
        shutil.move(excelfile, euroFilename)   # uncomment after testing


    if filename_only.startswith("Carexpert_Agent_Gesing"):
        renamefile_kw("Agenten_Stats_","_KW")
    elif filename_only.startswith("Hotlineber1458"):
        renamefile("1458_daily_")
    elif filename_only.startswith("CE_Out_taeglich"):
        renamefile("CE_Outbound_")
    elif filename_only.startswith("CE_alles_taeglich_83"):
        renamefile("CE_alle_Agenten_taeglich_")
    else:
        print("."),


if "single" in flag:
    print ("rename the file")
    rename_xls(sys.argv[1])
elif "multi" in flag:
    print ("begin processing dir")
    fullpath=os.path.abspath(sys.argv[1])
    allfiles=os.listdir(fullpath)
    for i in allfiles:
        fullfile=os.path.join(fullpath,i)
        rename_xls(fullfile)
