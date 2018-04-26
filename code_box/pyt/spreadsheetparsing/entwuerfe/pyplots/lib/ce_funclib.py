
# coding: utf-8

# In[1]:
import os,sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator, WeekdayLocator, MonthLocator, DayLocator, DateLocator, DateFormatter
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.ticker import AutoMinorLocator, AutoLocator, FormatStrFormatter, ScalarFormatter
import numpy as np
import datetime, calendar
from datetime import timedelta
import matplotlib.patches as mpatches
from itertools import tee

def testfunc():
    print('hi')

def determine_kernzeit(datum):
    ### Kernzeiten
    ### ab 01.03.2017: Mo-Fr 11:30-19:30
    ### ab 05.06.2017: Mo-Fr 8-20
    ### ab 08.07. plus Samstag 8-13
    weekday=datum.strftime('%a')
    #print(type(datum))
    #print(datum, weekday)

    if datum.date() < datetime.date(2017,3,1):
        bzeit = 'k'

    elif datetime.date(2017,3,1) <= datum.date() < datetime.date(2017,6,5):   ## Zeit zwischen 1.Maerz und 1. Juni
        if weekday in ("Sat", "Sun"): ## WE immer Nebenzeit
            bzeit = 'n'
        else:                           ## Werktage von 11:30 bis 19:30
            if datetime.time(11,30) <= datum.time() < datetime.time(19,30):
                bzeit = 'k'
            else:
                bzeit = 'n'

    elif datetime.date(2017,6,5) <= datum.date() < datetime.date(2017,7,8): ## Zeit ab 05.Juni bis 07. Juli
        if weekday in ("Sat", "Sun"): ## WE immer Nebenzeit
            bzeit = 'n'
        else:                           ## Werktage von 8-20
            if datetime.time(8,00) <= datum.time() < datetime.time(20,00):
                bzeit = 'k'
            else:
                bzeit = 'n'
    ### hier noch ab wann samstags 8-13 gezaehlt wird
    elif datum.date() >= datetime.date(2017,7,8): ## Zeit ab Sa, 08. Juli
        if weekday in ("Sun"): ## So. Nebenzeit
            bzeit = 'n'   
        elif weekday in ("Sat"): ## Sa. 8-13
            if datetime.time(8,00) <= datum.time() < datetime.time(13,00):
                bzeit = 'k'
            else:
                bzeit = 'n'
        else:                           ## Werktage von 8-20
            if datetime.time(8,00) <= datum.time() < datetime.time(20,00):
                bzeit = 'k'
            else:
                bzeit = 'n'

    return bzeit

def continuity_check(daten_liste):
    
    ### expects an array or a list of items to check
    ### returns either an empty list or a list of missing items
    
    sortedseries=sorted(daten_liste)
    
    datesmissing=list()
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b)
        return zip(a, b)

    for prev, curr in pairwise(sortedseries):
        i = prev
        #print(prev,curr)
        while i + datetime.timedelta(1) < curr:
            i += datetime.timedelta(1)
            datesmissing.append(i)
    return datesmissing

###############################
###### PRINT FUNCTIONS ########
###############################

def decminutes_to_mmss(decimal,*args, **kwargs):
    #print(decimal)
    tdelta=timedelta(minutes=decimal)
    sekunden=tdelta.seconds
    minuten=(sekunden % 3600) // 60
    restsekunden=str(sekunden %60).zfill(2)
    mmssstring='{}:{}'.format(minuten, restsekunden)
    return mmssstring

def maptix2labels(ticks):
    ylabelz=list()
    for tic in ticks:
        #print(tic)
        tic=abs(tic)
        sstr=decminutes_to_mmss(tic)
        ylabelz.append(sstr)
    return ylabelz

def plotit(zeiten, agent,ww_or_dd):
    bgkern='#FFF7F2'
    bgnebn='#F8FFF2'
    aht="#21a9ff"
    att="#ceecff"
    aac="#c4c4c4"
    zielzeit="#FF006E"
    bars="#A06A00"
    aav='#000C00'

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False, figsize=(17,7))
    
    ### entscheidung, ob die nach woche oder kalendertag sortierten spalten benutzt werden
    if ww_or_dd.lower() == 'woche':
        kzeit=zeiten[agent]['k_week'].copy()
        nzeit=zeiten[agent]['n_week'].copy()
    elif ww_or_dd.lower() == 'tage':
        kzeit=zeiten[agent]['k_day'].copy()
        nzeit=zeiten[agent]['n_day'].copy()
        
    ### check empty frames, leere frames werden mit Nullen gefuellt
    if (kzeit.empty and nzeit.empty):
        print('ueberhaupt keine Calls, Panik!')
    elif kzeit.empty:
        print('keine calls in der Kernzeit')
        kzeit=kzeit.reindex(nzeit.index)
        kzeit[['agent','ort','wd','yy','mm','id']]=nzeit[['agent','ort','wd','yy','mm','id']]# werden übernommen
        kzeit[['bz']]='k'
        kzeit.fillna(0,inplace=True)
        kzeit[['an','be','vl']].astype(np.int64)
    elif nzeit.empty:
        print('keine calls in der Nebenzeit')
        nzeit=nzeit.reindex(kzeit.index)
        nzeit[['agent','ort','wd','yy','mm','id']]=kzeit[['agent','ort','wd','yy','mm','id']]# werden übernommen
        nzeit[['bz']]='n'
        nzeit.fillna(0,inplace=True)
        nzeit[['an','be','vl']].astype(np.int64)
    
    ### get values for min, max, start, end, calls_sum, and mean 
    kmax=(kzeit['aht'].max())+0.5
    nmax=(nzeit['aht'].max())+0.5
    commonmax=max(kmax,nmax)
    commonmin=-0.25
    
    ersterZeitpunkt=min(min(kzeit.index),min(nzeit.index))
    letzterZeitpunkt=max(kzeit.index[-1],nzeit.index[-1])
    StartStr=str(ersterZeitpunkt)
    EndeStr=str(letzterZeitpunkt)
    
    calls_zeitraum_k=kzeit['be'].sum()
    calls_zeitraum_n=nzeit['be'].sum()
    
    htmean_k=kzeit['aht'].replace(0,np.NaN).mean()
    if np.isnan(htmean_k):
        htmean_k=0 # if the average is actually zero/nan, then deliberately set it to zero, otherwise labelmapping will complain
    htmean_n=nzeit['aht'].replace(0,np.NaN).mean() # decent mean value without the zeroes jan-mar
    if np.isnan(htmean_n):
        htmean_n=0 # if the average is actually zero/nan, then deliberately set it to zero, otherwise labelmapping will complain
    av_all_k=zeiten['Alle']['k_week']['aht'].replace(0,np.NaN).mean() # show mean of all agents
    av_all_n=zeiten['Alle']['n_week']['aht'].replace(0,np.NaN).mean() # show mean of all agents

    ### plots
    ax3 = ax1.twinx()
    ax3.tick_params('y', labelsize=6, labelcolor=bars)

    ax4 = ax2.twinx()
    ax4.tick_params('y', labelsize=6, labelcolor=bars)

    kcalls=ax3.bar(kzeit.index, kzeit['be'], width=0.7, alpha=0.1, color=bars, label='calls')
    ncalls=ax4.bar(nzeit.index, nzeit['be'], width=0.7, alpha=0.1, color=bars, label='calls')

    kaht,=ax1.plot(kzeit.index,kzeit['aht'],color=aht,label="aht")
    katt,=ax1.plot(kzeit.index,kzeit['att'],color=att,label="att")
    kacw,=ax1.plot(kzeit.index,kzeit['acw'],color=aac,label="acw")
    naht,=ax2.plot(nzeit.index,nzeit['aht'],color=aht,label="aht")
    natt,=ax2.plot(nzeit.index,nzeit['att'],color=att,label="att")
    nacw,=ax2.plot(nzeit.index,nzeit['acw'],color=aac,label="acw")

    kziel=ax1.axhline(y=3.5,color=zielzeit,ls=':',alpha=0.75, label='3:30 min')
    kreal=ax1.axhline(y=htmean_k,color=aht,ls='--',alpha=0.9, label=str(decminutes_to_mmss(htmean_k)))
    kalle=ax1.axhline(y=av_all_k,color=aav,ls='-.',alpha=0.2, label=str(decminutes_to_mmss(av_all_k)))
    nziel=ax2.axhline(y=1.5,color=zielzeit,ls=':',alpha=0.75, label='1:30 min')
    nreal=ax2.axhline(y=htmean_n,color=aht,ls='--',alpha=0.9, label=str(decminutes_to_mmss(htmean_n)))
    nalle=ax2.axhline(y=av_all_n,color=aav,ls='-.',alpha=0.2, label=str(decminutes_to_mmss(av_all_n)))

    ### ax1 labels
    ax1.set_ylim(commonmin,commonmax)

    minloc=AutoMinorLocator(4)
    ax1.yaxis.set_minor_locator(minloc)
    ax1.yaxis.set_minor_formatter(ScalarFormatter()) # is the same as major formatter

    left_tix_mj=ax1.get_yticks()
    left_tix_mn=ax1.get_yticks(minor=True)
    left_lbl_mj=maptix2labels(left_tix_mj)
    left_lbl_mn=maptix2labels(left_tix_mn)

    ax1.yaxis.set_ticklabels(left_lbl_mj)
    ax1.yaxis.set_ticklabels(left_lbl_mn,minor=True,size=6)

    ### ax2 labels
    ax2.set_ylim(ax1.get_ylim())

    ax2.yaxis.set_minor_locator(minloc)
    ax2.yaxis.set_minor_formatter(ScalarFormatter()) # is the same as major formatter

    left_tix_mj=ax2.get_yticks()
    left_tix_mn=ax2.get_yticks(minor=True)
    left_lbl_mj=maptix2labels(left_tix_mj)
    left_lbl_mn=maptix2labels(left_tix_mn)

    ax2.yaxis.set_ticklabels(left_lbl_mj)
    ax2.yaxis.set_ticklabels(left_lbl_mn,minor=True,size=6)

    ### color adjustments, titles, legend
    ax1.set_facecolor(bgkern)
    ax2.set_facecolor(bgnebn)

    desc_k,desc_n=str(int(calls_zeitraum_k)),str(int(calls_zeitraum_n))
    ax1.set_title('Kernzeit'+' Calls gesamt: '+desc_k, size=9)
    ax2.set_title('Nebenzeit'+' Calls gesamt: '+desc_n, size=9)

    ax1.set_xlabel(ww_or_dd, size=7)
    ax2.set_xlabel(ww_or_dd, size=7)
    ax1.tick_params('x', labelsize=6)
    ax2.tick_params('x', labelsize=6)

    ax1.set_ylabel('Minuten', rotation=90)
    ax4.set_ylabel('Calls',rotation=90,color=bars)

    
    ## hier sollte ein titel generiert werden, der dem Zeitraum entspricht
    f.suptitle('Bearbeitungszeiten '+agent+' nach '+ww_or_dd+' ab '+StartStr+' bis '+ww_or_dd+' '+EndeStr)
    f.legend((kaht,katt,kacw,kziel,kreal,kalle,kcalls),('handling','talk','afterwork','zielzeit','Øzeit agent','Øzeit alle','calls'),fontsize=7,ncol=2,loc='upper right',borderaxespad=2)

    
    
    ###Testing

    
    
    ### Abspeichern
    heute=datetime.date.today().strftime('%Y_%m_%d')
    bild_filename=str(heute+'_'+agent+'_'+ww_or_dd+'_'+StartStr+'-'+EndeStr)
    savepath='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/ce_teamleitung/plots/agenten_und_standorte/'
    speichernin=os.path.join(savepath,bild_filename)
    #print(speichernin)
    #f.savefig(speichernin,ext='png')
    #plt.close()
    return ax1,ax2
