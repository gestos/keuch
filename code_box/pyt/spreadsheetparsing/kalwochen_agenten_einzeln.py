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
            print kuerzel
	    id_num = int(teile.match(i).group(3).strip())
	    if not id_num in agent_id_set:
	        agent_id_set[id_num] = dict()
		agent_id_set[id_num]["standort"] = standort
		agent_id_set[id_num]["kuerzel"] = kuerzel
	except:
	    print("sth wrong with " + str(i))
    return agent_id_set

def check_cmdline_params():
    if len(sys.argv) != 3:
        print(sys.argv[0] +" needs two parameters in the following order: $DIR where xls files lie and an xls $FILE to write into.")
        print("will produce acd and acw stats for each agent in calendar-week blocks")
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
    print ("searching files called 'Agenten_Stats...'"),
    for i in os.listdir(filesdir):
        if i.startswith("Agenten_Stats"):
            print ("found "+str(i)+" "),
            agentsfiles.append(i)
    print
    return agentsfiles


def create_dic_from_all_files(agentsfiles):
    ag_monthly_dic = {}
    weeks_found = set()
    vorhandene_agenten = get_uniq_agents_multi(agentsfiles)
    teile = re.compile(r'(^\D)\s(.*)(\b\d[\d\s]*$)')

    for agent in vorhandene_agenten:
        agent_standor = teile.match(agent).group(1).strip()
        agent_kuerzel = teile.match(agent).group(2).strip()
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
                    weeks_found.add(calweek)
                    calls_this_hour=int(input_sheet.cell(row,4).value)
                    abgebrochne=int(input_sheet.cell(row,22).value)
                    bearbeitung=input_sheet.cell(row,24).value # die Zeiten bleiben nach dem Komma dezimal; geschrieben wird am Ende als Bruch /1440 = excel interne floating zahl, die eine Zeit ergibt
                    verbindung=input_sheet.cell(row,29).value
                    nacharbeit=bearbeitung-verbindung
                    ag_monthly_dic[agent]["calls"][timestamp] = [calweek, calls_this_hour, abgebrochne, bearbeitung, verbindung, nacharbeit]

    return ag_monthly_dic, weeks_found

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


def filter_weeks(startwoche, endwoche, source_dict):
    target_dict = {}    # empty dictionary to be filled and returned
    for woche in range(startwoche, endwoche+1):
        target_dict[woche] = {}
        for agent in source_dict:
            target_dict[woche][agent] = {}
            target_dict[woche][agent]["total"] = {}
            target_dict[woche][agent]["average"] = {}
            anrufe, abgebr, gesamtzeit, gespraechszeit, nacharbeitszeit = ([] for i in range(5))
            for timestamp in source_dict[agent]["calls"]:
                if source_dict[agent]["calls"][timestamp][0] == woche:
                    dataset = source_dict[agent]["calls"][timestamp]
                    anrufe.append(dataset[1]), abgebr.append(dataset[2]), gesamtzeit.append(dataset[3]), gespraechszeit.append(dataset[4]), nacharbeitszeit.append(dataset[5])
            agent_total_woche = list()
            agent_average_woche = list()

            for field in [anrufe, abgebr, gesamtzeit, gespraechszeit, nacharbeitszeit]:
                agent_total_woche.append(sum(field))
            if agent_total_woche[0] == 0:
                del target_dict[woche][agent] # von diesem Agenten wurden keine Anrufe angenommen, also fliegt er aus dem dictionary
            else:
                target_dict[woche][agent]["total"] = agent_total_woche

                anrufe_woche = sum(anrufe)
                av_gesamt = sum(gesamtzeit)/anrufe_woche
                av_telefon = sum(gespraechszeit)/anrufe_woche
                av_nacharb = sum(nacharbeitszeit)/anrufe_woche

                agent_average_woche.extend((av_gesamt, av_telefon, av_nacharb))
                target_dict[woche][agent]["average"] = agent_average_woche


        if not target_dict[woche]:
            del target_dict[woche]
    return target_dict

def filter_months(startmonat, endmonat, source_dict):
    target_dict = {}    # empty dictionary to be filled and returned
    for monat in range(startmonat, endmonat+1):
        target_dict[monat] = {}
        for agent in source_dict:
            target_dict[monat][agent] = {}
            target_dict[monat][agent]["total"] = {}
            target_dict[monat][agent]["average"] = {}
            anrufe, abgebr, gesamtzeit, gespraechszeit, nacharbeitszeit = ([] for i in range(5))
            for timestamp in source_dict[agent]["calls"]:
                if timestamp.month == monat:
                    dataset = source_dict[agent]["calls"][timestamp]
                    anrufe.append(dataset[1]), abgebr.append(dataset[2]), gesamtzeit.append(dataset[3]), gespraechszeit.append(dataset[4]), nacharbeitszeit.append(dataset[5])
            agent_total_monat = list()
            agent_average_monat = list()

            for field in [anrufe, abgebr, gesamtzeit, gespraechszeit, nacharbeitszeit]:
                agent_total_monat.append(sum(field))
            if agent_total_monat[0] == 0:
                del target_dict[monat][agent] # von diesem Agenten wurden keine Anrufe angenommen, also fliegt er aus dem dictionary
            else:
                target_dict[monat][agent]["total"] = agent_total_monat

                anrufe_monat = sum(anrufe)
                av_gesamt = sum(gesamtzeit)/anrufe_monat
                av_telefon = sum(gespraechszeit)/anrufe_monat
                av_nacharb = sum(nacharbeitszeit)/anrufe_monat

                agent_average_monat.extend((av_gesamt, av_telefon, av_nacharb))
                target_dict[monat][agent]["average"] = agent_average_monat


        if not target_dict[monat]:
            del target_dict[monat]
    return target_dict

def write_out(zeit_dict):

    xlwt.add_palette_colour("head_kern1", 0x21)
    target_workbook_writeable.set_colour_RGB(0x21, 106, 188, 255)
    xlwt.add_palette_colour("head_kern2", 0x22)
    target_workbook_writeable.set_colour_RGB(0x22, 171, 218, 255)
    xlwt.add_palette_colour("head_neben1", 0x23)
    target_workbook_writeable.set_colour_RGB(0x23, 236, 171, 255)
    xlwt.add_palette_colour("head_neben2", 0x24)
    target_workbook_writeable.set_colour_RGB(0x24, 227, 133, 255)
    xlwt.add_palette_colour("head_gesamt1", 0x25)
    target_workbook_writeable.set_colour_RGB(0x25, 169, 255, 133)
    xlwt.add_palette_colour("head_gesamt2", 0x26)
    target_workbook_writeable.set_colour_RGB(0x26, 131, 255, 79)

    if zeit_dict == weeks["kernzeit"]:
        sheet = target_workbook_writeable.get_sheet(0)
        startrow = target_workbook.sheet_by_index(0).nrows+1
        style_header1   = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color head_kern1')
        style_header2   = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color head_kern2')
    elif zeit_dict == weeks["nebenzeit"]:
        sheet = target_workbook_writeable.get_sheet(1)
        startrow = target_workbook.sheet_by_index(1).nrows+1
        style_header1   = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color head_neben1')
        style_header2   = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color head_neben2')
    elif zeit_dict == weeks["kern+neben"]:
        sheet = target_workbook_writeable.get_sheet(2)
        startrow = target_workbook.sheet_by_index(2).nrows+1
        style_header1   = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color head_gesamt1')
        style_header2   = xlwt.easyxf('alignment: horiz centre; pattern: pattern solid, fore_color head_gesamt2')

    weeks_in_dict = set()
    weeks_in_dict = set(sorted(zeit_dict))

    if max(weeks_in_dict) > max(weeks_in_target):
        print ("new weeks found")
        weeks_to_write = weeks_in_dict.difference(weeks_in_target)
    else:
        print (str(weeks_in_target)+" weeks are already present, nothing to write")
        exit()

    ask = raw_input("do you really want to overwrite [y/n]")[:1]
    if not ask.lower() == 'y':
        print("ok; bye :-)")
        exit()

    else:
        for calweek_k in sorted(weeks_to_write):
            sheet.write(startrow, 0, "", style_header2)   #Woche
            sheet.write(startrow, 1, "Kalenderwoche", style_header2)   #Woche
            sheet.write(startrow, 2, calweek_k, style_header2)   #Woche
            sheet.write(startrow, 3, "", style_header2)   #Woche
            sheet.write(startrow, 4, "", style_header2)   #Woche
            sheet.write(startrow, 5, "", style_header2)   #Woche
            startrow += 1
            sheet.write(startrow, 0, "Standort", style_header1)
            sheet.write(startrow, 1, "Agent", style_header1)
            sheet.write(startrow, 2, "Angenommene", style_header1)
            sheet.write(startrow, 3, "Ges.Zeit", style_header1)
            sheet.write(startrow, 4, "Tel.Zeit", style_header1)
            sheet.write(startrow, 5, "Nachb.Zeit", style_header1)
            startrow += 1
            for agent in sorted(zeit_dict[calweek_k].keys()):
                excelzeit=list()
                for zeit in zeit_dict[calweek_k][agent]['average']:
                    excelzeit.append(zeit/1440)

                sheet.write(startrow, 0, all_data[agent]["standort"], style_week)    #Standort
                sheet.write(startrow, 1, agent, style_week)    #Agent
                sheet.write(startrow, 2, zeit_dict[calweek_k][agent]["total"][0], style_week)    #Anzahl der angenommenen
                sheet.write(startrow, 3, excelzeit[0], style_times)    # Av_Gesamtzeit
                sheet.write(startrow, 4, excelzeit[1], style_times)    #Av_Telefonzeit
                sheet.write(startrow, 5, excelzeit[2], style_times)    #Av_Nacharbeit
                startrow += 1
            startrow += 1
    target_workbook_writeable.save(targetfile)

def find_target_maxweek(book_to_write_to):
    all_times = book_to_write_to.sheet_by_index(2)
    rows = all_times.nrows
    weeks_found_in_target = set()
    if not rows:
        print("nothing there")
        weeks_found_in_target.add(0)
    for row in range(0,rows):
        if "Kalenderwoche" in all_times.cell(row,1).value:
            weeks_found_in_target.add(int(all_times.cell(row,2).value))
        else:
            weeks_found_in_target.add(0)
    return weeks_found_in_target
##########################################################################
##############START OF PROGRAM############################################
##########################################################################

filesdir,targetfile         = check_cmdline_params()
agentsfiles                 = get_agent_reports(filesdir)
all_data,weeks_found        = create_dic_from_all_files(agentsfiles) ## this will gives us every row of every agents_stats file available into one big dict
alle_agenten                = all_data.keys()
data_kernzeit,data_nebenzeit = split_zeiten(all_data)  ## now we have two separate dicts for kern and nebenzeit

weeks = {}
weeks["kernzeit"] = filter_weeks(1, 53, data_kernzeit)  # hier bitte noch bei der all_data generierung die start-kalenderwoche und die max_kalenderwoche rausholen
weeks["nebenzeit"] = filter_weeks(1, 53, data_nebenzeit)
weeks["kern+neben"] = filter_weeks(1, 53, all_data)

months = {}
months["kernzeit"] = filter_months(1, 3, data_kernzeit)
months["nebenzeit"] = filter_months(1, 3, data_nebenzeit)
months["kern+neben"] = filter_months(1, 3, all_data)


#####################  START WRITEOUT ####################



target_workbook = xlrd.open_workbook(targetfile, formatting_info=True)  # this is the file
target_workbook_writeable = xlcopy.copy(target_workbook)                # a copy is needed to write into


weeks_in_target=find_target_maxweek(target_workbook)
print type(weeks_in_target)
print weeks_in_target




style_week      = xlwt.easyxf('alignment: horiz centre')
style_times     = xlwt.easyxf('alignment: horiz centre', num_format_str = "HH:MM:SS")


write_out(weeks["kernzeit"])
write_out(weeks["nebenzeit"])
write_out(weeks["kern+neben"])

