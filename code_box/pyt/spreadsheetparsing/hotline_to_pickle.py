#!/usr/bin/python3
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime
import numpy as np


def check_cmdline_params():
    if len(sys.argv) != 3:
        print(sys.argv[0])
        print(textwrap.fill("1. Argument muss ein Verzeichnis oder eine HOTLINEstatistik (nicht Agenten- oder Terminierungsstatistik) sein. Diese muss viertelstuendlich aufgedroeselt sein, um eine Trennung nach Kern- und Nebenzeiten zu ermoeglichen.",80))
        print
        print(textwrap.fill("2. Argument ist die Ziel-Pickle-Datei",80))
        print
        print(textwrap.fill("Beispiel mit jetzigem Setup: ./programm[0] test_stats/archiv/ [1] pickle_hotline.pkl [2] ",280))
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
        #sys.stdout.write(spinner.next())  # write the next character
        sys.stdout.write(next(spinner))  # write the next character, hopefully py3
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
    return agentsfiles

def read_entries(datei,doe):
    sheet = xlrd.open_workbook(datei, formatting_info=True).sheet_by_index(0)
    out_dict = dict()
    kern_start = datetime.time(11,30)
    kern_end = datetime.time(19,15)
    teststring=sheet.cell(3,0).value

    if teststring != 'Timestamp':
        print('terrible flaw')
        exit()

    if sheet.nrows < 4:
        print ("that's a file without entries")
        print (datei)
        exit()
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

        doe[stamp] = dict()
        o = doe[stamp]
        o["tm"] = stamp.time()
        o["dt"] = stamp.date()
        o["yy"] = year
        o["mm"] = int(month)
        o["dd"] = int(day)
        o["xl"] = xldate
        o["hh"] = int(hour)
        o["bz"] = bzeit
        o["ww"] = int(week)
        o["wd"] = weekday
        o["an"] = int(angeboten)
        o["vb"] = int(verbunden)
        o["vl"] = int(verloren)
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
    print (dayframe_sum.iloc[0]['dt'],','),
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
    print (day,', ', end='', flush=True)
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

    if hours_frame.loc['summa','angekommen'] == 0:
        print('fatal exception, set SLA to NaN, no calls for this day?')
        hours_frame.loc['summa','servicelevel'] = np.NaN
    else:
        hours_frame.loc['summa','servicelevel'] =  hours_frame.loc['summa','verbunden']/hours_frame.loc['summa','angekommen']

    hours_frame = hours_frame.T
    hours_frame['xlday'] = day
    hours_frame['day'] = datemap[day]['day']
    hours_frame['date'] = datemap[day]['date']
    hours_frame['week']= dayframe.loc[0,'ww']
    hours_frame['weekday']= datemap[day]['weekday']
    hours_frame['month']= datemap[day]['month']
    hours_frame['year']= datemap[day]['year']

    cols=hours_frame.columns.tolist()
    cols.insert(0, cols.pop())
    cols.insert(0, cols.pop())

    hours_frame=hours_frame[cols]

    return hours_frame

def write_out(df_sum,target_workbook_w):

    global s_row
    row=s_row-1
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
    style_2dec              = xlwt.easyxf('alignment: horiz centre', num_format_str = '0.00')
    style_verlo             = xlwt.easyxf('alignment: horiz centre; font: color gray25')
    style_minuten           = xlwt.easyxf('alignment: horiz centre', num_format_str = "[M]:SS")

    global s_row2 # we've collected this already from sheet[1]
    row=s_row2-1
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

        val_an = series_an[i] # everything else is ok with xlwt...
        sheet_angenommen.write(row, i, val_an, style) 

        val_vl = series_vl[i] # everything else is ok with xlwt...
        sheet_verloren.write(row, i, val_vl, style) 

        val_sla = series_sla[i] # everything else is ok with xlwt...
        if i == 27:
            style = style_2dec
        sheet_sla.write(row, i, val_sla, style) 

    target_workbook_w.save(target)
    s_row2 += 1

def datemapper(datelist):
    mapdict = dict()
    for datum in sorted(dates_in_dir):
        xldate=excel_date(datum)
        mapdict[xldate] = dict()
        mapdict[xldate]['date'] = datum
        mapdict[xldate]['year'] = datum.year
        mapdict[xldate]['month'] = datum.month
        mapdict[xldate]['week'] = datum.strftime('%W')
        mapdict[xldate]['day'] = datum.day
        mapdict[xldate]['weekday'] = datum.strftime('%a')
    return mapdict
####################end of function definitions#####################
source,target,pmode = check_cmdline_params()
doe = dict()    # dict of everything, from here all selections (by agent, by agent and date, by hours etc) are possible

## read everything from directory into a dict and create a dataframe from it
if pmode == "dir":
    filelist=get_filelist(source)
    print('dictionary creation...',end='',flush=True)
    for k in sorted(filelist.keys()):
        doe = read_entries(filelist[k],doe)
    print('ready')
elif pmode == "file":
    doe = read_entries(source,doe)

print('dictionary to pandas dataframe...')
column_order = ['tm','dt','yy','mm','ww','wd','dd','xl','hh','an','vb','vl','ht','tt','acw','bz']
doe_frame = pandas.DataFrame(doe).T[column_order] # This df contains ALL files that were scanned in the input_dir
dates_in_dir = doe_frame.dt.unique()    # numpy.ndarray of datetime.date objects
xldates_in_dir = doe_frame.xl.unique()    # numpy.ndarray of datetime.date objects
years_in_dir = doe_frame.yy.unique()    # numpy.ndarray of year values
kws_in_dir = doe_frame.ww.unique()      # numpy.ndarray of week numbers
monate_in_dir = doe_frame.mm.unique()   # numpy.ndarray of month numbers
datemap = datemapper(dates_in_dir)
df_alldays = pandas.DataFrame()
print('ok')

print('create stats for each day...')
for day in xldates_in_dir:
    df_sla = create_hourly_stats(day)
    df_alldays = pandas.concat([df_alldays, df_sla])
print('ok')

print
df_alldays.to_pickle(sys.argv[2])