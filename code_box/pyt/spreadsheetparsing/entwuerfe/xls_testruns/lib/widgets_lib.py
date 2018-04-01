
# coding: utf-8

# In[1]:

## Import necessary modules
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

sys.path.append(os.path.abspath('/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/entwuerfe/xls_testruns/lib/'))
from ce_funclib import determine_kernzeit as dtkz
from ce_funclib import continuity_check
from ce_funclib import decminutes_to_mmss, maptix2labels, plotit

from ipywidgets import widgets, interact, interactive, fixed, interact_manual, Layout
from IPython.display import display
#%matplotlib inline
get_ipython().magic('matplotlib tk')


## Import data frome pickle generated from muß ein file mit agentenstats sein
arcpth='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/test_stats/archiv/'


# In[2]:

######## GET A LIST OF MATCHING .xls FILES FROM THE GIVEN DIRECTORY


# In[3]:

def collectxlfiles(arcpath):
    xlfilelist=list()

    for xlfile in os.listdir(arcpath):
        if xlfile.startswith('CE_al'):
            xlfileabs=os.path.join(arcpath,xlfile)
            xlfilelist.append(xlfileabs)
    return sorted(xlfilelist)

xlfilelist=collectxlfiles(arcpth)
#xlfilelist
#examplefile=xlfilelist[233]


# In[4]:

###### TEST FOR DATA IN FILE, SORT OUT EMPTY FILES 


# In[5]:

## good dataframes do per definition not contain any zero values
## fill bad DFs with nan?

def filetoframe(exfile):
    exframe=pd.read_excel(exfile) # this is a regular pd.DataFrame
    datecell=exframe.iloc[0,1]
    sheet_datetime=pd.to_datetime(datecell,format='%d.%m %Y : %H')
    sheet_date=sheet_datetime.date()
    
    integritycheck=exframe.iloc[2,1] # files with data have "agenten" here, files with no calls have a 'nan'

    if integritycheck != 'Agenten':
        # if it's empty, keep date for filling it later
        print('Exception: ', end='')
        except_status='ex'
        
        usefulcols={0:'tstamp',1:'agent',3:'an',4:'be',22:'vl',24:'ht_float',29:'tt_float'} # map cols to decent names
        exframe=exframe.reindex(columns=sorted(usefulcols.keys()))
        exframe.rename(columns=usefulcols,inplace=True)        
        exframe=exframe[0:1] # strip text rows and the mangled sum row
        print(sheet_datetime)
        
        exframe['tstamp']=sheet_datetime
        exframe['date']=sheet_date
        exframe['agent']='nocalls_datum'
        exframe[['wd','ww','mm','yy']]=exframe['tstamp'].dt.strftime('%a,%W,%m,%Y').str.split(',',expand=True) # make ww,yy,mm,wd columns
        exframe['bz']=exframe['tstamp'].apply(dtkz)
        exframe['ort']=exframe['agent'].str[0] # split the identifier into useable columns
        exframe['id']='foobar' # split the identifier into useable columns
        
        # integers should be of appropriate datatype, we received them as strings
        # exframe[['vl','an','be','ww','mm','yy']]=exframe[['vl','an','be','ww','mm','yy']].astype(np.int64) #just for the beauty of it
        exframe.fillna(0, inplace=True) 
        exframe[['ww','mm','yy']]=exframe[['ww','mm','yy']].astype(np.int64) #just for the beauty of it
        #exframe.fillna(0, inplace=True) 
        return exframe,except_status
        
    else:
        except_status='reg'
        
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
        
        # integers should be of appropriate datatype, we received them as strings
        exframe[['vl','an','be','ww','mm','yy']]=exframe[['vl','an','be','ww','mm','yy']].astype(np.int64) #just for the beauty of it

        return exframe,except_status


# In[6]:

example_badframe,badstatus=filetoframe('/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/test_stats/archiv/CE_alle_Agenten_taeglich_2017-04-17.xls')
example_goodframe,goodstatus=filetoframe('/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/test_stats/archiv/CE_alle_Agenten_taeglich_2017-05-17.xls')
example_badframe


# In[7]:

example_goodframe.head(3)


# In[8]:

framelist=list()
exceptionlist=list()
for xfile in xlfilelist:
    
    #print('file:',xfile)
    frame_from_file,except_status=filetoframe(xfile)
    #print(frame_from_file.columns)
    #print(frame_from_file['date'])
    if except_status=='ex':
        exceptionlist.append(xfile)
    framelist.append(frame_from_file)

exceptionlist


# In[ ]:




# In[9]:

#### produce a unified frame with all data and sort it by timstamp and agentname
bigframeii=pd.concat(framelist)

bigframeii.sort_values(['tstamp','agent'],inplace=True)
bigframeii.reset_index(drop=True,inplace=True) # there you go


# In[10]:

# bigframeii
# die exklusivlogins müssen zusammengelegt werden
unify_id={'gesinst':'995887','stanzju':'878457','papkeda':'891914'}
bigframeii.loc[bigframeii['id'] == unify_id['gesinst'],'agent'] = 'gesinst'
bigframeii.loc[bigframeii['id'] == unify_id['stanzju'],'agent'] = 'stanzju'
bigframeii.loc[bigframeii['id'] == unify_id['papkeda'],'agent'] = 'papkeda'


# In[11]:

### some date locator play, can conveniently be checked against a single xls file
#def check_single_day(day):
#    dayvalues=bigframeii.loc[bigframeii['date'] == day]
#    print('htsum',dayvalues['ht_float'].sum(), end=', ')
#    print('bearbeitete sum',dayvalues['be'].sum())
#check_single_day(datetime.date(2017,4,17)) # shows that days wihtout calls are in the frame, too
#check_single_day(datetime.date(2017,4,18)) # shows that days wihtout calls are in the frame, too


# In[12]:

#### get all dates and check whether they're contiguous
datenserie_uniq=bigframeii['date'].unique().tolist()
tage_bestand=len(datenserie_uniq)
tage_start=datenserie_uniq[0]
tage_ende=datenserie_uniq[-1:]

missing_dates=continuity_check(datenserie_uniq)
if not missing_dates:
    print('no dates are missing')
else:
    print('the following dates are not within the frame:')
    print(missing_dates)


# In[13]:

### PARSE AGENT DATA
### What I want:
### * get a list of all agents that have worked in the period 
### * get data for each agent
### * get average of all agents as a reference
### per agent:
### ** get all calls that have lasted longer than x times the average of all agents
### ** get a plot of all calls (by timestamp)
### ** get a plot of all days (by date)
### ** get their tendencies over the weeks (? vacation dates missing and so on)

#bigframeii.tail(10)


# In[14]:

# get all agents available and create frames for kern and neben
allagents_list=sorted(bigframeii['agent'].unique())
allagents_list.extend(['Hagenow','Berlin','Alle'])
standorte=bigframeii.ort.unique().tolist()

bigk=bigframeii.loc[bigframeii['bz']=='k']
bign=bigframeii.loc[bigframeii['bz']=='n']


# **we can't figure out individual calls anyway, since raw data calls have been grouped by hours already  
# so we can go on and group by days to figure out averages**

# In[ ]:




# In[15]:

def group_and_add_average(agentname,frame,gruppierung):
    # step one: filter by agent; if agent is a location-bound group, filter by location and change agent name to group name
    if agentname == 'Hagenow':
        nur_agent=frame.loc[frame['ort']=='H'].copy()
        nur_agent['agent']='Hagenow'
        nur_agent['id']='000001'
    elif agentname == 'Berlin':
        nur_agent=frame.loc[frame['ort']=='B'].copy()
        nur_agent['agent']='Berlin'
        nur_agent['id']='000002'
    elif agentname == 'Alle':
        #nur_agent=frame.loc[frame['ort'].isin(standorte)].copy()
        nur_agent=frame.copy()
        nur_agent['agent']='Alle'
        nur_agent['id']='000000'    
    else:
        nur_agent=frame.loc[frame['agent']==agentname]
    

    # step 2: split into kern and neben
    k=nur_agent.loc[nur_agent['bz']=='k']
    if k.empty:
        print()
        print(agentname,end=' ')
        print('keine Kernzeit group_and_add_average')
        print('###')
        
    n=nur_agent.loc[nur_agent['bz']=='n']
    if n.empty:
        print()
        print(agentname,end=' ')
        print('keine Nebenzeit group_and_add_average')
        print('###')

    # step 3: group by day (instead of hour, as it is now) and add average ht,tt
    def group_and_average(agframe):
        ### ttstamp is dropped and date will be the new index; all others summed or reduced
        colfx_day={'agent':'first','an':'sum','be':'sum','vl':'sum','ht_float':'sum','tt_float':'sum','wd':'first','ww':'first', 'mm':'first','yy':'first','bz':'first','ort':'first','id':'first'}
        ### ttstamp is dropped, date is dropped and ww will be the new index; all others summed or reduced
        colfx_week={'agent':'first','an':'sum','be':'sum','vl':'sum','ht_float':'sum','tt_float':'sum','wd':'first','mm':'first','yy':'first','bz':'first','ort':'first','id':'first'}
        
        if gruppierung=='tag':
            grpd=agframe.groupby('date').agg(colfx_day)
        elif gruppierung=='woche':
            grpd=agframe.groupby('ww').agg(colfx_week)
        elif gruppierung=='nursplit':
            grpd=agframe.copy()
        
        grpd['aht']=grpd['ht_float']/grpd['be']
        grpd['att']=grpd['tt_float']/grpd['be']
        grpd['acw']=grpd['aht']-grpd['att']

        return grpd

    # step 4 get stats grouped by day and with the average column
    k_agent=group_and_average(k)
    n_agent=group_and_average(n)

    return k_agent,n_agent


# **dictionary of frames**

# In[16]:

### generate frames grouped by day and by week for every agent, put them in a dictionary
zeiten={}
print('collecting and grouping times (neben, kern) for')
for namen in allagents_list:
    kern_byday,neben_byday=group_and_add_average(namen,bigframeii,'tag')
    kern_byweek,neben_byweek=group_and_add_average(namen,bigframeii,'woche')

    zeiten[namen]={'k_day':kern_byday,'k_week':kern_byweek,'n_day':neben_byday,'n_week':neben_byweek}


# In[17]:

# zeiten['haustst']['n_day']


# In[23]:

#### isin function is pretty neat thing for filtering
#### obviously, ww is another datatype than mm, normalization required!
zeiten['gesinst']['n_day'].loc[zeiten['gesinst']['n_day']['ww'].isin([32,33,34,35,36,37,38,39,40,41])]


# In[19]:

def get_sortlist(frame,sortby):
    print(sortby.lower())
    overall_funx1={'be':'sum','ht_float':'sum'}
    gesframe=frame.groupby('agent').agg(overall_funx1).copy()
    gesframe['aht']=(gesframe['ht_float']/gesframe['be'])

    overall_funx2={'be':'sum','ht_float':'sum'}
    ortsframe=frame.loc[bigframeii['ort'].isin(['H','B'])].groupby('ort').agg(overall_funx2).copy()
    ortsframe['aht']=(ortsframe['ht_float']/ortsframe['be'])

    newf=ortsframe.rename(index={'B':'berlin','H':'hagenow'})
    newf.index.names=['agent']
    newfall=pd.concat([gesframe,newf]).fillna(0)
    if sortby.lower() == 'calls':
        newfall.sort_values('be',ascending=False,inplace=True)
    elif sortby.lower() == 'aht':
        newfall.sort_values('aht',ascending=False,inplace=True)
    
    #print(newfall)
    
    return newfall.index.tolist()


# In[20]:

# hier erstmal die Daten
dats=sorted(bigframeii.date.unique())

# aufsetzen der Widgets, die in die Boxen kommen: 
agtsortmethod=widgets.RadioButtons(options=['Calls', 'avAHT'],value='Calls',description='Agenten sortiert nach:',disabled=False)
agent_chooser=widgets.SelectMultiple(options=get_sortlist(bigframeii,agtsortmethod.value),layout=Layout(display="flex", flex_flow='column'),description='Agents',disabled=False)
ww_dd_chooser=widgets.RadioButtons(options=['Wochen', 'Einzeltage'],value='Wochen',description='Gruppierung:',disabled=False)
whichweeks=widgets.IntRangeSlider(step=1,disabled=False,min=1,max=52,value=[1,52],description='Wochen')
fromdt=widgets.SelectionSlider(options=dats,description='Von:')
tilldt=widgets.SelectionSlider(options=dats, min=fromdt.value,max=dats[-1],description='Bis:')
gobutton=widgets.Button(description='Click me',disabled=False,button_style='',tooltip='Click me',icon='check')

# layout der widget-boxen
overbox=widgets.HBox(description='outer box',title='outer box', name='outer box', layout=Layout(border='2px solid black'))             # Das ist der Hauptcontainer, in den die weiteren Boxen kommen
leftbox_agents=widgets.VBox(layout=Layout(border='2px solid blue'))      # linke Box innerhalb
rightbox_timeranges=widgets.VBox(layout=Layout(border='2px solid purple')) # rechte Box innerhalb
overbox.children=[leftbox_agents,rightbox_timeranges]               # so werden die Boxen im Container platziert
leftbox_agents.children=[agtsortmethod,agent_chooser]               # widgets für die linke Box
rightbox_timeranges.children=[ww_dd_chooser,whichweeks,gobutton]    # widgets für die rechte Box

# 'observe'-Funktionen für die widgets:
def shift_tilldt(args):
    farom=dats.index(args['new'])
    tilldt.options=dats[farom:]
def switchflick(args):
    wd=args['new']
    #print(wd)
    #print(rightbox_timeranges)
    if wd=='Einzeltage':
        rightbox_timeranges.children=[ww_dd_chooser,fromdt,tilldt,gobutton]
    elif wd=='Wochen':
        rightbox_timeranges.children=[ww_dd_chooser,whichweeks,gobutton]
def agtsort(args):
    sor=(args['new'])
    #print(sor)
    if sor.lower() == 'calls':
        agent_chooser.options=get_sortlist(bigframeii,'calls')
    elif sor.lower() == 'avaht':
        agent_chooser.options=get_sortlist(bigframeii,'aht')
def passvalues(args):
    agenten=agent_chooser.value
    wwdd=ww_dd_chooser.value
    zeitrahmen=dict()
    if wwdd.lower()=='wochen':
        zeitrahmen['wochen']=whichweeks.value
    elif wwdd.lower()=='einzeltage':
        zeitrahmen['vonbis']=fromdt.value,tilldt.value
    printparams=tuple([agenten,wwdd,zeitrahmen])
    print(printparams)
    return printparams

# Zuweisung/Bindung der 'observe'-Funktionen an die widgets
agtsortmethod.observe(agtsort,'value') 
# Erklärung: das widget 'agtsortmethod' hat als potentielle Values die beiden Werte,
# die oben beim Start des Widgets als "Options" hinterlegt wurden ("Calls" und "avAHT")
# wird das widget betätigt, wird sie funktion "agtsort" mit dem gerade gewählten Wert als Parameter aufgerufen
# die Funktion setzt in einem anderen widget (agent_chooser) die zur Auswahl stehenden Werte direkt
ww_dd_chooser.observe(switchflick,'value')
fromdt.observe(shift_tilldt,'value')
gobutton.on_click(passvalues)

display(overbox)


# In[21]:

#plotit(printargs)
agtsortmethod.value


# In[22]:

plotit(zeiten, 'gesinst', 'woche')   ## funktioniert, aber zeitraum muß vorher noch gesetzt werden


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



