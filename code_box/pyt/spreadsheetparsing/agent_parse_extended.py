#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar
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

def parsedate_full(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.value # comes like this from upstream, date always lives at 1,1
    day, mon, yea, hou, mnt = date_crap[1:3], date_crap[4:6], date_crap[7:11], date_crap[12:14], date_crap[15:17]
    date_clea=str(day+"."+mon+"."+yea+"."+hou)
    date_objt = datetime.strptime(date_clea, "%d.%m.%Y.%H") # this is a python datetime.date object
    return date_objt

def get_uniq_agents(startrow, endrow, sheet):
    ag_ids = set()
    for i in range(startrow,endrow):
        ag_id = str(sheet.cell(i,1).value)
        ag_ids.add(ag_id)
    return ag_ids

def get_uniq_agents_multi (agentsfiles):
    ag_ids = set()
    for datei in agentsfiles:
        full_file = os.path.join(filesdir,datei)
        input_sheet = xlrd.open_workbook(full_file, formatting_info=True).sheet_by_index(0)
        rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
        startrow = 4            #die ersten 4 sind der fixe header, Daten beginnen bei Reihe 5 (in xlrd mit index 0 = 4)
        endrow = rows_read-1    #letzte Reihe ist eine "Summe"-Reihe, Daten enden eine Reihe darueber
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

def average_stats(calweek, ag_dic, startrow, endrow, input_sheet):
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

def check_sheet_type(sheet):
    if sheet.cell(0,0).value.startswith("Carexpert_Agent_Gesing"):
        flag="agent_stats"
    elif sheet.cell(0,0).value.startswith("Hotlineber1458"):
        flag="hotline_stats"
    return flag

def get_agent_reports(filesdir):
    agentsfiles = list()
    for i in os.listdir(filesdir):
        if i.startswith("Agenten_Stats"):
            agentsfiles.append(i)
    return agentsfiles

def create_report_by_week(agentsfiles):
    for i in agentsfiles:

        full_file = os.path.join(filesdir,i)
        input_sheet = xlrd.open_workbook(full_file, formatting_info=True).sheet_by_index(0)

        if "agent_stats" not in check_sheet_type(input_sheet): # determine by title-cell (always 0,0) what type of datasheet this is
            print("not an agent report sheet, skipping")
            exit()

        rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
        startrow = 4            #die ersten 4 sind der fixe header, Daten beginnen bei Reihe 5 (in xlrd mit index 0 = 4)
        endrow = rows_read-1    #letzte Reihe ist eine "Summe"-Reihe, Daten enden eine Reihe darueber
        sheet_startdate = parsedate(input_sheet.cell(1,1)) # gives a set of date-object(YY,MM,DD) xlint, calendarweek
        sheet_enddate = parsedate(input_sheet.cell(2,1))
        sheet_calweek = "%0*d" % (2, parsedate(input_sheet.cell(1,1))[2]) # calendar week with a leading zero

        weeks[sheet_calweek] = {}

        vorhandene_agenten = get_uniq_agents(startrow, endrow, input_sheet)
        ag_dic = {}

        for i in vorhandene_agenten:
            agent_kuerzel = i[2:9]
            agent_standor = i[0]
            ag_dic[agent_kuerzel] = {}
            ag_dic[agent_kuerzel]["standort"] = agent_standor

        average_stats(sheet_calweek, ag_dic, startrow, endrow, input_sheet)
        #### use return values from average_stats() to fill dictionary ####
        weeks[sheet_calweek] = ag_dic

def create_dic_from_all_files(agentsfiles):
    ag_monthly_dic = {}
    vorhandene_agenten = get_uniq_agents_multi(agentsfiles)

    for agent in vorhandene_agenten:
        agent_kuerzel = agent[2:9]
        agent_standor = agent[0]
        ag_monthly_dic[agent_kuerzel] = {}
        ag_monthly_dic[agent_kuerzel]["standort"] = agent_standor
        ag_monthly_dic[agent_kuerzel]["calls"] = dict()

    for i in agentsfiles:
        full_file = os.path.join(filesdir,i)
        input_sheet = xlrd.open_workbook(full_file, formatting_info=True).sheet_by_index(0)

        if "agent_stats" not in check_sheet_type(input_sheet): # determine by title-cell (always 0,0) what type of datasheet this is
            print("not an agent report sheet, skipping")
            exit()

        rows_read, cols_read = input_sheet.nrows, input_sheet.ncols
        startrow = 4            #die ersten 4 sind der fixe header, Daten beginnen bei Reihe 5 (in xlrd mit index 0 = 4)
        endrow = rows_read-1    #letzte Reihe ist eine "Summe"-Reihe, Daten enden eine Reihe darueber
        sheet_startdate = parsedate(input_sheet.cell(1,1)) # gives a set of date-object(YY,MM,DD) xlint, calendarweek
        sheet_enddate = parsedate(input_sheet.cell(2,1))

        for agent in ag_monthly_dic:
            for row in range(startrow, endrow):
                if agent in input_sheet.cell(row,1).value:
                    timestamp=parsedate_full(input_sheet.cell(row,0))
                    datum=timestamp.strftime("%Y-%b-%d %H")
                    calweek = timestamp.isocalendar()[1]
                    calls_this_hour=int(input_sheet.cell(row,4).value)
                    abgebrochne=int(input_sheet.cell(row,22).value)
                    bearbeitung=input_sheet.cell(row,24).value # die Zeiten bleiben nach dem Komma dezimal; geschrieben wird am Ende als Bruch /1440 = excel interne floating zahl, die eine Zeit ergibt
                    verbindung=input_sheet.cell(row,29).value
                    nacharbeit=bearbeitung-verbindung
                    ag_monthly_dic[agent]["calls"][timestamp] = [calweek, calls_this_hour, abgebrochne, bearbeitung, verbindung, nacharbeit]

    return ag_monthly_dic

def split_zeiten(all_data):
    kernzeit = {}
    nebenzeit = {}

    for agent in sorted(all_data):
        kernzeit[agent] = {}
        kernzeit[agent]["standort"] = all_data[agent]["standort"]
        kernzeit[agent]["calls"] = {}
        nebenzeit[agent] = {}
        nebenzeit[agent]["standort"] = all_data[agent]["standort"]
        nebenzeit[agent]["calls"] = {}

        for entry in all_data[agent]["calls"]:
            if 11 <= entry.hour <=19:
                kernzeit[agent]["calls"][entry] = all_data[agent]["calls"][entry]
            else:
                nebenzeit[agent]["calls"][entry] = all_data[agent]["calls"][entry]

    return kernzeit, nebenzeit


def datenfilter_per_monat(agent, monat, neben_oder_kern):
    wunschdir = {}
    wunschdir[agent] = {}
    wunschdir[agent]["standort"] = neben_oder_kern[agent]["standort"]
    wunschdir[agent]["calls"] = { key: value for key, value in neben_oder_kern[agent]["calls"].items() if key.month == monat } # BEI RANGE gilt immer die zweite Zahl NICHT included. Range fuer 2 ist 2,3 !!!
    #wunschdir[agent]["calls"] = { key: value for key, value in neben_oder_kern[agent]["calls"].items() if key.month == monat }
    return wunschdir




##########################################################################
##############START OF PROGRAM############################################
##########################################################################

filesdir,targetfile = check_cmdline_params()
agentsfiles = get_agent_reports(filesdir)
weeks = {}
months = {}
# create_report_by_week(agentsfiles) # this produces a dictionary that can be used for weekly output
all_data=create_dic_from_all_files(agentsfiles) ## this will gives us every row of every agents_stats file available into one big dict
data_kernzeit, data_nebenzeit = split_zeiten(all_data)  ## now we have two separate dicts for kern and nebenzeit

for month in range(1,3):    # RANGE CUTS THE LAST ELEMENT! so it's always range (start, end+1)!
    monthname = calendar.month_abbr[month]
    mname = calendar.month_abbr[month]
    for agent in data_nebenzeit.keys():
        monthname = datenfilter_per_monat(agent, month, data_nebenzeit)
        if not monthname[agent]["calls"]:
            print (str(agent) + " is empty HAS BEEN REMOVED")
            del monthname[agent]
            continue
        print ("daten fuer " + agent + " in nebenzeit" + mname + " :" + str(month)),
        print len(monthname[agent]["calls"])   # This result is correct

    for agent in data_kernzeit.keys():
        monthname = datenfilter_per_monat(agent, month, data_nebenzeit)
        if not monthname[agent]["calls"]:
            print (str(agent) + " is empty HAS BEEN REMOVED")
            del monthname[agent]
            continue
        print ("daten fuer " + agent + " in kernzeit" + mname + " :" + str(month)),
        print len(monthname[agent]["calls"])   # This result is correct
        print monthname
print monthname

## ! now to do : thinking of what to do with data ;-)

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

#write_out(start_writing)

