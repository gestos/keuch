#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime


def check_cmdline_params():
    if len(sys.argv) != 3:
        print(sys.argv[0])
        print(textwrap.fill("1. Argument muss ein Verzeichnis oder eine HOTLINEstatistik (nicht Agenten- oder Terminierungsstatistik) sein. Diese muss viertelstuendlich aufgedroeselt sein, um eine Trennung nach Kern- und Nebenzeiten zu ermoeglichen.",80))
        print
        print(textwrap.fill("2. Argument ist die Ziel-Exceldatei, dorthin wird die generierte Zeile unten eingefuegt",80))
        print
        print(textwrap.fill("Beispiel mit jetzigem Setup: ./programm[0] test_stats/archiv/1458_daily_2017-03-08.xls[1] taegliche_hotline_halbstunden.xls[2] ",280))
        exit()
    elif not os.path.isfile(sys.argv[1]):
        if os.path.isdir(sys.argv[1]):
            pmode="dir"
            sourcefile_IB = os.path.abspath(sys.argv[1])
            targetfile = os.path.abspath(sys.argv[2])
            print("source inbound:\t" + sourcefile_IB)
            print("target:\t" + targetfile)
            return sourcefile_IB, targetfile, pmode
        else:
            print(sys.argv[1]+" is not a regular file")
            exit()
    elif not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + " is not a regular file")
        exit()
    else:
        pmode="file"
        sourcefile_IB = os.path.abspath(sys.argv[1])
        targetfile = os.path.abspath(sys.argv[2])
        print("source inbound:\t" + sourcefile_IB)
        print("target:\t" + targetfile)
        return sourcefile_IB, targetfile, pmode

def parsedate_full(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea, hou, mnt = date_crap[0:2], date_crap[3:5], date_crap[6:10], date_crap[11:13], date_crap[14:16]
    date_clea=str(day+"."+mon+"."+yea+"."+hou+"."+mnt)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y.%H.%M") # this is a python datetime.date object
    return date_objt

def parsedate_header(daily_sheet_cell): # turn crap date into nice date
    date_crap = daily_sheet_cell.strip() # comes like this from upstream, date always lives at 1,1
    day, mon, yea = date_crap[0:2], date_crap[3:5], date_crap[6:10]
    date_clea=str(day+"."+mon+"."+yea)
    date_objt = datetime.datetime.strptime(date_clea, "%d.%m.%Y") # this is a python datetime.date object
    return date_objt

def excel_date(date1):
    temp = datetime.date(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def get_filelist(folder):
    print ("scanning " + str(folder) + " "),
    agentsfiles = dict()
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    for i in (s for s in os.listdir(folder) if s.endswith(".xls")):
        sys.stdout.write(spinner.next())  # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')
        datei = os.path.join(folder,i)
        sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
        if sheet.nrows == 0:
            continue
        if sheet.cell(0,0) and (sheet.cell(0,0).value == "Hotlineber1458Gesing taegl" or sheet.cell(0,1).value == "1458 carexpert Kfz-Sachverstae"):
            #if sheet.cell(0,0) and sheet.cell(0,0).value == "CE_alles_taeglich":
            sheet_date = parsedate_header(sheet.cell(1,1).value).date() # this will be the dictionary key as it is the unique overall key
            agentsfiles[sheet_date] = datei
    print
    return agentsfiles

def read_entries(datei,doe):
    sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
    out_dict = dict()
    kern_start = datetime.time(11,30)
    kern_end = datetime.time(19,15)
    if sheet.nrows < 3:
        print ("that's a file without entries")
        return

    rows = sheet.nrows
    for i in range(4,sheet.nrows-1):
        stamp = parsedate_full(sheet.cell(i,0).value)
        year = stamp.year
        month = stamp.month
        day = stamp.day
        week = int(stamp.isocalendar()[1])
        weekday = stamp.strftime('%a')
        hour = stamp.hour

        if weekday in ("Sat", "Sun"):
            bzeit = "n"
        elif kern_start <= stamp.time() <= kern_end:
            bzeit = "k"
        else:
            bzeit = "n"

        angeboten = sheet.cell(i,2).value
        verbunden = sheet.cell(i,3).value
        verloren = angeboten - verbunden
        tt = sheet.cell(i,5).value
        acw = sheet.cell(i,12).value
        ht = tt + acw
        
        xldate=excel_date(stamp.date())

        if angeboten > 0:
            doe[stamp] = dict()
            o = doe[stamp]
            o["tm"] = stamp.time()
            o["dt"] = stamp.date()
            o["yy"] = year
            o["mm"] = month
            o["dd"] = day
            o["xl"] = xldate
            o["hh"] = hour
            o["bz"] = bzeit
            o["ww"] = int(week)
            o["wd"] = weekday
            o["an"] = angeboten
            o["vb"] = verbunden
            o["vl"] = verloren
            o["tt"] = tt
            o["ht"] = ht
            o["acw"] = acw
    return doe

def target_days_found(sheet,srow):
    found_days = [0]
    s = sheet
    for row in range (2,srow-1):
        c = s.cell(row,0)
        if c.value:
            found_days.append(c.value)
    return found_days

def create_summary(day):
    dayframe = doe_frame.loc[doe_frame['xl'] == day].reset_index()
    colfunx={'dt':'first' , 'ww':'first', 'an':'sum' , 'vb':'sum' , 'vl':'sum' , 'ht':'sum' , 'tt':'sum' , 'acw':'sum'}
    dayframe_sum = dayframe.groupby('xl').agg(colfunx)
    print dayframe_sum.iloc[0]['dt'],',',
    dayframe_sum['tot_av_tt'] = dayframe_sum['tt'] / dayframe_sum['vb']
    dayframe_sum['tot_av_ht'] = dayframe_sum['ht'] / dayframe_sum['vb']
    dayframe_sum['tot_av_acw'] = dayframe_sum['acw'] / dayframe_sum['vb']

    nzeit = dayframe[dayframe['bz'] == 'n']
    nzeit_sum = nzeit.groupby('xl').agg(colfunx)
    nzeit_sum['n_av_tt'] = nzeit_sum['tt'] / nzeit_sum['vb']
    nzeit_sum['n_av_ht'] = nzeit_sum['ht'] / nzeit_sum['vb']
    nzeit_sum['n_av_acw'] = nzeit_sum['acw'] / nzeit_sum['vb']

    kzeit = dayframe[dayframe['bz'] == 'k']
    kzeit_sum = kzeit.groupby('xl').agg(colfunx)
    kzeit_sum['k_av_tt'] = kzeit_sum['tt'] / kzeit_sum['vb']
    kzeit_sum['k_av_ht'] = kzeit_sum['ht'] / kzeit_sum['vb']
    kzeit_sum['k_av_acw'] = kzeit_sum['acw'] / kzeit_sum['vb']

    dayframe_sum['k_vb'] = kzeit_sum['vb']
    dayframe_sum['k_vl'] = kzeit_sum['vl']
    dayframe_sum['k_av_tt'] = kzeit_sum['k_av_tt']
    dayframe_sum['k_av_ht'] = kzeit_sum['k_av_ht']
    dayframe_sum['k_av_acw'] = kzeit_sum['k_av_acw']

    dayframe_sum['n_vb'] = nzeit_sum['vb']
    dayframe_sum['n_vl'] = nzeit_sum['vl']
    dayframe_sum['n_av_tt'] = nzeit_sum['n_av_tt']
    dayframe_sum['n_av_ht'] = nzeit_sum['n_av_ht']
    dayframe_sum['n_av_acw'] = nzeit_sum['n_av_acw']

    del dayframe_sum['ht']
    del dayframe_sum['tt']
    del dayframe_sum['acw']
    col_order_daysum = ['dt','ww','vl','vb','tot_av_ht', 'tot_av_tt', 'tot_av_acw', 'k_vl', 'k_vb', 'k_av_ht', 'k_av_tt', 'k_av_acw', 'n_vl', 'n_vb', 'n_av_ht', 'n_av_tt', 'n_av_acw']
    dayframe_sum = dayframe_sum[col_order_daysum].fillna(0)
    return dayframe_sum


def create_hourly_stats(day):
    print day,
    dayframe = doe_frame.loc[doe_frame['xl'] == day].reset_index()
    hours_index = dict()
    for i in range (0,25):
        hours_index[i] = dict()
        hours_index[i]["angekommen"] = 0
        hours_index[i]["verbunden"] = 0
        hours_index[i]["verloren"] = 0
        hours_index[i]["servicelevel"] = 0
    hours_frame = pandas.DataFrame(hours_index).T # df for 0:00-0:30, 0:30-1:30 ... 23:30-23:59
    hours_frame['tix'] = ["00:00-00:30",'00:30-01:30','01:30-02:30','02:30-03:30','03:30-04:30','04:30-05:30','05:30-06:30','06:30-07:30','07:30-08:30','08:30-09:30','09:30-10:30','10:30-11:30','11:30-12:30','12:30-13:30','13:30-14:30','14:30-15:30','15:30-16:30','16:30-17:30','17:30-18:30','18:30-19:30','19:30-20:30','20:30-21:30','21:30-22:30','22:30-23:30','23:30-00:00']
    hours_frame=hours_frame[['tix','angekommen','verbunden','verloren','servicelevel']]

    for ix, datarow in dayframe.iterrows():
        tstamp=datarow['tm']
        hour_ix = tstamp.hour
        if 0 <= tstamp.minute < 30:
            hour_mod = 0
        else:
            hour_mod = 1
        hour_ix = hour_ix+hour_mod
        hours_frame.ix[hour_ix,'angekommen'] += datarow['an']
        hours_frame.ix[hour_ix,'verbunden'] += datarow['vb']
        hours_frame.ix[hour_ix,'verloren'] += datarow['vl']

    hours_frame['servicelevel'] = hours_frame['verbunden']/hours_frame['angekommen']
    hours_frame.loc['summa','angekommen'] = hours_frame['angekommen'].sum()
    hours_frame.loc['summa','verbunden'] = hours_frame['verbunden'].sum()
    hours_frame.loc['summa','verloren'] = hours_frame['verloren'].sum()
    hours_frame.loc['summa','servicelevel'] = hours_frame['servicelevel'].mean()
    hours_frame = hours_frame.T
    hours_frame['day'] = day
    hours_frame['week']= dayframe.loc[0,'ww']

    cols=hours_frame.columns.tolist()
    cols.insert(0, cols.pop())
    cols.insert(0, cols.pop())

    hours_frame=hours_frame[cols]

    return hours_frame

def write_out(df_sum,target_workbook_w):

    global s_row
    row=s_row
    sheet_rw = target_workbook_w.get_sheet(0)
    
    style_datum             = xlwt.easyxf('alignment: horiz right', num_format_str = "ddd, dd.mm.yy")
    style_kw_trenner        = xlwt.easyxf('alignment: horiz right; font: color 0x17; borders: right double, right_color 0x28')
    style_number            = xlwt.easyxf('alignment: horiz centre')
    style_verlo             = xlwt.easyxf('alignment: horiz centre; font: color gray25')
    style_minuten           = xlwt.easyxf('alignment: horiz centre', num_format_str = "[M]:SS")

    ix=df_sum.index
    columns=df_sum.columns


    sheet_rw.write(row, 0, ix[0], style_datum)   #Datum
    sheet_rw.write(row, 1, int(df_sum.iloc[0]['ww']), style_kw_trenner)   #Woche

    sheet_rw.write(row, 3, df_sum.iloc[0]['vl'], style_verlo)   # Verlorene Total
    sheet_rw.write(row, 4, df_sum.iloc[0]['vb'], style_number)   # Verbundene Total
    sheet_rw.write(row, 5, df_sum.iloc[0]['tot_av_ht'], style_minuten)   # Av. HT Total
    sheet_rw.write(row, 6, df_sum.iloc[0]['tot_av_tt'], style_minuten)   # Av. TT Total
    sheet_rw.write(row, 7, df_sum.iloc[0]['tot_av_acw'], style_minuten)   # Av. ACW Total
    
    sheet_rw.write(row, 9, df_sum.iloc[0]['k_vl'], style_verlo)   # Verlorene Total
    sheet_rw.write(row, 10, df_sum.iloc[0]['k_vb'], style_number)   # Verbundene Total
    sheet_rw.write(row, 11, df_sum.iloc[0]['k_av_ht'], style_minuten)   # Av. HT Total
    sheet_rw.write(row, 12, df_sum.iloc[0]['k_av_tt'], style_minuten)   # Av. TT Total
    sheet_rw.write(row, 13, df_sum.iloc[0]['k_av_acw'], style_minuten)   # Av. ACW Total

    sheet_rw.write(row, 15, df_sum.iloc[0]['n_vl'], style_verlo)   # Verlorene Total
    sheet_rw.write(row, 16, df_sum.iloc[0]['n_vb'], style_number)   # Verbundene Total
    sheet_rw.write(row, 17, df_sum.iloc[0]['n_av_ht'], style_minuten)   # Av. HT Total
    sheet_rw.write(row, 18, df_sum.iloc[0]['n_av_tt'], style_minuten)   # Av. TT Total
    sheet_rw.write(row, 19, df_sum.iloc[0]['n_av_acw'], style_minuten)   # Av. ACW Total

    target_workbook_w.save(target)
    s_row += 1

def write_sla(hours_frame,workbook):
    style_datum             = xlwt.easyxf('alignment: horiz right', num_format_str = "ddd, dd.mm.yy")
    style_kw_trenner        = xlwt.easyxf('alignment: horiz right; font: color 0x17; borders: right double, right_color 0x28')
    style_number            = xlwt.easyxf('alignment: horiz centre')
    style_verlo             = xlwt.easyxf('alignment: horiz centre; font: color gray25')
    style_minuten           = xlwt.easyxf('alignment: horiz centre', num_format_str = "[M]:SS")

    global s_row2 # we've collected this already from sheet[1]
    row=s_row2
    sheet_angenommen = workbook.get_sheet(1)
    sheet_verloren = workbook.get_sheet(2)
    sheet_sla = workbook.get_sheet(3)

    series_an = hours_frame.loc['verbunden'].values
    series_vl = hours_frame.loc['verloren'].values
    series_sla = hours_frame.loc['servicelevel'].values

    for i in range(0,len(series_an)):
        if i == 0:
            style = style_datum
        elif i == 1:
            style = style_kw_trenner
        else:
            style = style_number

        if i in [0,1]:
            val_an = series_an[i].item()  # numpy.int64 can not be written with xlwt...
        else:
            val_an = series_an[i] # everything else is ok with xlwt...
        sheet_angenommen.write(row, i, val_an, style) 

        if i in [0,1]:
            val_vl = series_vl[i].item()
        else:
            val_vl = series_vl[i]
        sheet_verloren.write(row, i, val_vl, style) 

        if i in [0,1]:
            val_sla = series_sla[i].item()
        else:
            val_sla = series_sla[i]
        sheet_sla.write(row, i, val_sla, style) 

    target_workbook_w.save(target)
    s_row2 += 1

####################end of function definitions#####################
source,target,pmode = check_cmdline_params()
doe = dict()    # dict of everything, from here all selections (by agent, by agent and date, by hours etc) are possible

## read everything from directory into a dict and create a dataframe from it
if pmode == "dir":
    filelist=get_filelist(source)
    for k in sorted(filelist.keys()):
        doe = read_entries(filelist[k],doe)

column_order = ['tm','dt','yy','mm','ww','wd','dd','xl','hh','an','vb','vl','ht','tt','acw','bz']
doe_frame = pandas.DataFrame(doe).T[column_order] # This df contains ALL files that were scanned in the input_dir
dates_in_dir = doe_frame.dt.unique()    # numpy.ndarray of datetime.date objects
xldates_in_dir = doe_frame.xl.unique()    # numpy.ndarray of datetime.date objects
years_in_dir = doe_frame.yy.unique()    # numpy.ndarray of year values
kws_in_dir = doe_frame.ww.unique()      # numpy.ndarray of week numbers
monate_in_dir = doe_frame.mm.unique()   # numpy.ndarray of month numbers

target_workbook = xlrd.open_workbook(target, formatting_info=True)  # this is the file
target_sheet = target_workbook.sheet_by_index(0)
target_workbook_w = xlcopy.copy(target_workbook)                # a copy is needed to write into
s_row = target_sheet.nrows+1

last_day_target = max(target_days_found(target_sheet,s_row)) # returns the highest date found as an excel date number
days_to_add = [i for i in xldates_in_dir if i > last_day_target] # list of days in scanned directory that are newer than the last day of the target sheet

print 'days found in dir: ',xldates_in_dir[:2], '...', xldates_in_dir[-2:]
print ('last day of current excelfile: '),last_day_target
print ('datasets to be appended: '),days_to_add

    
print 'writing to sheet 0 days ',
for day in days_to_add:
    print day,
    day_summary=create_summary(day)  ## creates a summary of a day from the overall doe_frame
    write_out(day_summary,target_workbook_w)
print
print ("finished writing sheet 0")
print


## process second sheet

target_sheet1 = target_workbook.sheet_by_index(1)
s_row2 = target_sheet1.nrows+1  # I'll just assume that sheets 1-3 are always the same date
last_day_target = max(target_days_found(target_sheet1,s_row2)) # returns the highest date found as an excel date number
days_to_add = [i for i in xldates_in_dir if i > last_day_target] # list of days in scanned directory that are newer than the last day of the target sheet

print 'last day of sla_statistics sheets: ',last_day_target
print 'datasets_sla to be appended: ',days_to_add[:2],'...',days_to_add[-2:]

print 'writing to sheets 1-3 days',
for day in days_to_add:
    df_sla = create_hourly_stats(day)
    df_sla.fillna('.', inplace=True)
    write_sla(df_sla,target_workbook_w)


print 'TOTAL SLA IS FAULTY! NEEDS TO BE ADJUSTED TO TOTAL NUMBER OF CALLS INSTEAD OF JUST HOURS'
print 'HOURLY SLA IS CORRECT!'
