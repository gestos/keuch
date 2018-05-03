#!/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/entwuerfe/ve/bin/python3
# coding: utf-8

# In[1]:

#get_ipython().magic('load_ext autoreload')
#get_ipython().magic('autoreload 2')

## Import necessary modules
import os,sys
import pandas as pd
import pickle
#import matplotlib.pyplot as plt
#from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator, WeekdayLocator, MonthLocator, DayLocator, DateLocator, DateFormatter
#from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
#from matplotlib.ticker import AutoMinorLocator, AutoLocator, FormatStrFormatter, ScalarFormatter
import numpy as np
import datetime, calendar
from datetime import timedelta
#import matplotlib.patches as mpatches
from itertools import tee, cycle
from traitlets import traitlets

sys.path.append(os.path.abspath('/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/entwuerfe/pyplots/lib/'))
from ce_funclib import determine_kernzeit as dtkz
from ce_funclib import continuity_check


# ## Agenten
# ### Deklarationen
## Lese-Verzeichnis, in dem die Agenten-Reports liegen
pth_read_1458='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/datenhalde/1458/'
pth_read_agents='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/datenhalde/alle_agents_taeglich/'
## Schreib-Verzeichnis, in das der gesammelte pickle abgelegt werden soll
pklpth='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/datenhalde/datapickles/'
heute=datetime.date.today().strftime('%Y-%m-%d')

spinner = cycle(['-', '\\', '|', '/'])
def spin():
    sys.stdout.write(next(spinner))  # write the next character, hopefully py3
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    sys.stdout.write('\b')

# ### Funktionen
######## GET A LIST OF MATCHING .xls FILES FROM THE GIVEN DIRECTORY
def collectfiles(pfad,welche):
    if welche == 'agents':
        startstring = 'CE_alle_Ag'
    elif welche == '1458':
        startstring = '1458_daily'
    else:
        return 'bitte angeben, welche Art Files gelesen werden soll (agents oder hotlinenummer)'

    xlfilelist=list()

    print('collecting '+welche)

    for xlfile in os.listdir(pfad):
        if xlfile.startswith(startstring):
            xlfileabs=os.path.join(pfad,xlfile)
            xlfilelist.append(xlfileabs)
            spin()
    print()
    return sorted(xlfilelist)

def makeniceframe(ixframe):        ## funktion nimmt einen mit daten befüllten frame und bringt ihn in eine vernünftige form
    exframe=ixframe.copy()

    exframe.columns=range(0,30) # rename columns to a temporarily more readable format, fancy rename later
    usefulcols={0:'tstamp',1:'agent',3:'an',4:'be',22:'vl',24:'ht_float',29:'tt_float'} # map cols to decent names
    exframe=exframe[sorted(usefulcols.keys())] # skip cols and keep the ones we need
    exframe.rename(columns=usefulcols,inplace=True) # rename cols
    exframe=exframe[3:-1] # strip text rows and the mangled sum row
    exframe['tstamp']=pd.to_datetime(exframe['tstamp'],format=' %d.%m.%Y %H:%M ')
    exframe['date']=exframe['tstamp'].dt.date
    exframe[['wd','ww','mm','yy']]=exframe['tstamp'].dt.strftime('%a,%W,%m,%Y').str.split(',',expand=True) # make ww,yy,mm,wd columns
    exframe['bz']=exframe['tstamp'].apply(dtkz)

    exframe['ort']=exframe['agent'].str[0] # split the identifier into useable columns
    exframe['id']=exframe['agent'].str[-6:] # split the identifier into useable columns
    exframe['agent']=exframe['agent'].str[2:-7] # split the identifier into useable columns

    #### trying unification while parse
    unify_id={'gesinst':'995887','stanzju':'878457','papkeda':'891914'}
    exframe.loc[exframe['id'] == unify_id['gesinst'],'agent'] = 'gesinst'
    exframe.loc[exframe['id'] == unify_id['stanzju'],'agent'] = 'stanzju'
    exframe.loc[exframe['id'] == unify_id['papkeda'],'agent'] = 'papkeda'

    # integers should be of appropriate datatype, we received them as strings
    exframe[['vl','an','be','ww','mm','yy']]=exframe[['vl','an','be','ww','mm','yy']].astype(np.int64) #just for the beauty of it

    spin()
    return exframe

def parse_filelist_to_dataframe(liste):
    print('merge files into one dataframe')

    liste_leerer_tage=list()
    bigframe=pd.DataFrame()

    for datei in liste:
        spin()
        readframe=pd.read_excel(datei)

        if len(readframe.columns) == 3:           # Dateien mit nur 3 Spalten enthalten keine Call-Daten
            #print('empty ', end='')
            liste_leerer_tage.append(datei)

        elif len(readframe.columns) == 30:
            #print('. ', end='')
            niceframe=makeniceframe(readframe)
            bigframe=bigframe.append(niceframe)

        else:
            print('Datei zum Nachgucken, hat weder 3 noch 30 Spalten')

    bigframe.sort_values(by='tstamp', inplace=True) # ganzen frame nach Uhrzeiten sortieren
    bigframe.set_index('tstamp',inplace=True) # timestamp als neuer Index

    print()
    return bigframe,liste_leerer_tage


# ### Filescraping und Roh-Dataframe
filelist_agents=collectfiles(pth_read_agents,'agents')
big_frame,leeretage=parse_filelist_to_dataframe(filelist_agents)
# ### Abspeichern
big_frame.to_pickle(pklpth+'Rohdaten_Agenten-'+heute+'.pkl')
print('saved to '+pklpth+'Rohdaten_Agenten-'+heute+'.pkl')

big_frame.to_pickle(pklpth+'Rohdaten_Agenten_aktuell.pkl')
print('saved to '+pklpth+'Rohdaten_Agenten_aktuell.pkl')

with open(pklpth+'Rohdaten_Agenten_Leertage'+heute, 'wb') as f:
    pickle.dump(leeretage, f)


# ## 1458

# ### Deklarationen Hotline_1458
neededcols=[0,1,2,3,5,12,21] # Liste der Spalten, die aus dem Excelfile gelesen werden sollen
new_colnames=['tstp','clls','ange','verb','tt','acw','lost'] # Namen, die spaeter auf die Spalten kommen
shitcols=('Verbindungszeit [hh:mm:ss]','Nachbearbeitungszeit [hh:mm:ss]')
converts={shitcols[0]:str,shitcols[1]:str}
ipynb_name='1458_allrounder'


# ### Funktionen 1458
def turn_xls_to_df(file):
    spin()

    excel_df=pd.read_excel(file,skiprows=3,skip_footer=1,usecols=neededcols,converters=converts)# die ersten 3 werden nicht benötigt, letzte auch nicht
    excel_df['Timestamp'] = pd.to_datetime(excel_df['Timestamp'], format=' %d.%m.%Y %H:%M ') # statt string soll das ein datetime werden
    excel_df.columns=new_colnames
    excel_df2=excel_df.set_index('tstp').copy() # die timestamps sollen der index sein

    return excel_df2

filelist_1458=collectfiles(pth_read_1458,'1458')

greatframe=pd.DataFrame() # leeren df initialisieren


print('merge hotline data to one dataframe')
for i in filelist_1458:
    i_frame=turn_xls_to_df(i)
    greatframe=greatframe.append(i_frame)
print()
# alle files werden ordentlich in df konvertiert und an den ausserhalb der funktion kreierten df angehangen
# greatframe # hier sind alle daten vollständig enthalten, die gebraucht werden, der Ur-Frame

print('reshaping und kern-/nebenzeit stamps')
## Anrufzeiten statt datetime oder string nach timedelta (Sekunden) gewandelt
greatframe[['tt','acw']]=greatframe[['tt','acw']].apply(pd.to_timedelta).astype('timedelta64[s]')
greatframe['ht'] = (greatframe['tt']+greatframe['acw'])
spin()
## add kern- und nebenzeit column
greatframe['bz'] = greatframe.index.map(dtkz)
spin()

greatframe.to_pickle(pklpth+'Rohdaten_1458-'+heute+'.pkl')
print('saved to '+pklpth+'Rohdaten_1458-'+heute+'.pkl')
greatframe.to_pickle(pklpth+'Rohdaten_1458_aktuell.pkl')
print('saved to '+pklpth+'Rohdaten_1458_aktuell.pkl')
#with open(pklpth+'Rohdaten_Agenten_Leertage'+heute, 'wb') as f:
#    pickle.dump(leeretage, f)
