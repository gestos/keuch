#!/usr/bin/python
import os
import csv
import math
import xlrd
import re
import sys
import xlwt
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import datetime,date


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

def parsedate(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.value # comes like this from upstream, date always lives at 1,1
    date_clea = re.sub(r' ', '.', date_crap[:10]) # transform to a string that strptime can parse
    date_objt = datetime.strptime(date_clea, "%d.%m.%Y").date() # this is a python datetime.date object
    xlint = (date_objt - date(1899, 12, 30)).days # this is an integer that excel uses internally
    calweek = date_objt.isocalendar()[1]
    return date_objt, xlint, calweek

def get_uniq_agents():
    ag_ids = set()
    for i in range(startrow,endrow):
        ag_id = str(input_sheet.cell(i,1).value)
        ag_ids.add(ag_id)
    return ag_ids

def parseminutes(cellstring): # turn crap time into nice hh:mm:ss
    dec_s,minute = math.modf(cellstring)
    seconds= round(((dec_s*60)/100),2)
    if minute < 60:
        zeit=minute+seconds
        time_objt = datetime.strptime(str(zeit), "%M.%S").time() # this is a python datetime.date object
    elif minute >= 60:
        hhmm=str('{:02d}:{:02d}'.format(*divmod(int(minute), 60)))
        ss=str("%0*d" % (2,int(seconds*100)))
        zeit=str(hhmm+":"+ss)
        time_objt = datetime.strptime(str(zeit), "%H:%M:%S").time() # this is a python datetime.date object
    return time_objt

def verbose_stats():
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

def average_stats(calweek):
    for ag in ag_dic:
        angenommene = []
        abgebrochne = []
        bearbeitung = []
        verbindung  = []
        for i in range(startrow,endrow):
            if ag in input_sheet.cell(i,1).value:
                angenommene.append(input_sheet.cell(i,4).value)
                abgebrochne.append(input_sheet.cell(i,22).value)
                bearbeitung.append(input_sheet.cell(i,24).value)
                verbindung.append(input_sheet.cell(i,29).value)
        av_bearb = sum(bearbeitung)/sum(angenommene)
        av_verbi = sum(verbindung)/sum(angenommene)
        av_nacha = av_bearb-av_verbi
        ag_dic[ag]["calls"]= int((sum(angenommene)))
        ag_dic[ag]["ges_bea"]= parseminutes(sum(bearbeitung))
        ag_dic[ag]["av_bearbeitung"]= parseminutes(av_bearb)
        ag_dic[ag]["av_verbindung"]= parseminutes(av_verbi)
        ag_dic[ag]["av_nacharbeit"]= parseminutes(av_nacha)

def check_sheet_type():
    if input_sheet.cell(0,0).value.startswith("Carexpert_Agent_Gesing"):
        flag="agent_stats"
    elif input_sheet.cell(0,0).value.startswith("Hotlineber1458"):
        flag="hotline_stats"
    return flag

def get_agent_reports(filesdir):
    agentsfiles = list()
    for i in os.listdir(filesdir):
        if i.startswith("Agenten_Stats"):
            agentsfiles.append(i)
    return agentsfiles
##########################################################################
##############START OF PROGRAM############################################
##########################################################################

filesdir,targetfile = check_cmdline_params()
agentsfiles = get_agent_reports(filesdir)
weeks = {}

for i in agentsfiles:

    full_file = os.path.join(filesdir,i)
    input_sheet = xlrd.open_workbook(full_file, formatting_info=True).sheet_by_index(0)

    if "agent_stats" not in check_sheet_type(): # determine by title-cell (always 0,0) what type of datasheet this is
        print("not an agent report sheet, skipping")
        exit()

    rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
    startrow = 4            #die ersten 4 sind der fixe header, Daten beginnen bei Reihe 5 (in xlrd mit index 0 = 4)
    endrow = rows_read-1    #letzte Reihe ist eine "Summe"-Reihe, Daten enden eine Reihe darueber
    sheet_startdate = parsedate(input_sheet.cell(1,1)) # gives a set of date-object(YY,MM,DD) xlint, calendarweek
    sheet_enddate = parsedate(input_sheet.cell(2,1))
    sheet_calweek = "%0*d" % (2, parsedate(input_sheet.cell(1,1))[2]) # calendar week with a leading zero

    weeks[sheet_calweek] = {}

    vorhandene_agenten = get_uniq_agents()
    ag_dic = {}
    
    for i in vorhandene_agenten:
        agent_kuerzel = i[2:9]
        agent_standor = i[0]
        ag_dic[agent_kuerzel] = {}
        ag_dic[agent_kuerzel]["standort"] = agent_standor
    
    average_stats(sheet_calweek)
    #### use return values from average_stats() to fill dictionary ####

    weeks[sheet_calweek] = ag_dic

#####################  START WRITEOUT ####################



target_workbook = xlrd.open_workbook(targetfile, formatting_info=True)
target_workbook_writeable = xlcopy.copy(target_workbook)
targetsheet = target_workbook.sheet_by_index(0)
sheet_rw = target_workbook_writeable.get_sheet(0)
start_writing = targetsheet.nrows

style_week              = xlwt.easyxf('alignment: horiz centre')
style_times           = xlwt.easyxf('alignment: horiz centre', num_format_str = "HH:MM:SS")


def write_out(startrow):
    ask = raw_input("do you really want that? [y/n]")[:1]
    if not ask.lower() == 'y':
        print("ok; bye :-)")
        exit()
    else:
        for calweek in sorted(weeks):
            for agent in sorted(weeks[calweek].keys()):
                sheet_rw.write(startrow, 0, calweek, style_week)   #Woche
                sheet_rw.write(startrow, 1, weeks[calweek][agent]["standort"], style_week)    #Standort
                sheet_rw.write(startrow, 2, agent, style_week)    #Standort
                sheet_rw.write(startrow, 3, weeks[calweek][agent]["calls"], style_week)    #Standort
                sheet_rw.write(startrow, 4, weeks[calweek][agent]["ges_bea"], style_times)    #Standort
                sheet_rw.write(startrow, 5, weeks[calweek][agent]["av_verbindung"], style_times)    #Standort
                sheet_rw.write(startrow, 6, weeks[calweek][agent]["av_nacharbeit"], style_times)    #Standort
                sheet_rw.write(startrow, 7, weeks[calweek][agent]["av_bearbeitung"], style_times)    #Standort
                startrow += 1
            startrow += 1
        target_workbook_writeable.save(targetfile)

write_out(start_writing)

